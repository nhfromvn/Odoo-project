import json
from odoo import http, fields
from odoo.http import request
import hmac
import hashlib
import requests
import werkzeug
import os
import jinja2
from pytz import timezone
from datetime import datetime
import shopify, binascii, json, string, random

SCOPES = '''read_products,
          read_customers,
          write_customers,
          read_third_party_fulfillment_orders,
          write_third_party_fulfillment_orders,
          read_orders,
          write_orders,
          write_draft_orders,
          read_draft_orders,
          write_script_tags,
          read_shipping,
          read_themes,
          write_themes,
          read_price_rules'''


class ShopifyController(http.Controller):
    @http.route('/bought-together/install', auth='user')
    def install_bought_together(self, **kwargs):
        print(kwargs)
        shop_url = kwargs['shop']
        api_key = request.env['ir.config_parameter'].sudo().get_param('shopify.api_key')
        state = kwargs['hmac']
        callback = request.env['ir.config_parameter'].sudo().get_param(
            'web.base.url') + '/bought-together/oauth/callback'

        url = f"https://{shop_url}/admin/oauth/authorize?client_id={api_key}&scope={SCOPES}&redirect_uri={callback}&state={state}&grant_options[]=per-user"
        return werkzeug.utils.redirect(url)

    @http.route('/bought-together/oauth/callback', type="http", auth="user", website=True, method=['GET'], csrf=False)
    def bought_together_callback(self, **kwargs):
        print(kwargs)
        if 'code' in kwargs:
            code = kwargs['code']

            if 'shop' in kwargs:
                shop_url = kwargs['shop']
            else:
                return json.dumps({
                    "error": "not found shop_url in response"
                })

            api_key = request.env['ir.config_parameter'].sudo().get_param('shopify.api_key')
            secret = request.env['ir.config_parameter'].sudo().get_param('shopify.secret_key')
            base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')

            headers = {'Content-Type': 'application/json'}
            body = {
                "client_id": api_key,
                "client_secret": secret,
                "code": code
            }
            # try:
            vals = {}
            url = 'https://' + shop_url + '/admin/oauth/access_token'

            res = requests.post(url=url, headers=headers, data=json.dumps(body))
            if res.status_code == 200:
                data = res.json()
                request.session['shop_url'] = shop_url
                vals['first_name'] = data['associated_user']['first_name']
                vals['last_name'] = data['associated_user']['last_name']
                vals['shop_url'] = shop_url
                vals['email'] = data['associated_user']['email']
                vals['locale'] = data['associated_user']['locale']
                vals['access_token'] = data['access_token']
                vals['code'] = code
                current_company = request.env['res.company'].sudo().search([('name', '=', kwargs['shop'])], limit=1)
                current_user = request.env['res.users'].sudo().search([('login', '=', kwargs['shop'])], limit=1)
                password_generate = ''.join(random.choice(string.ascii_letters) for i in range(20))
                print(password_generate)
                if not current_company:
                    current_company = request.env['res.company'].sudo().create({
                        'logo': False,
                        'currency_id': 2,
                        'sequence': 10,
                        'name': kwargs['shop'],
                        'street': False,
                        'street2': False,
                        'city': False,
                        'state_id': False,
                        'zip': False,
                        'country_id': False,
                        'phone': False,
                        'email': False,
                        'website': False,
                        'vat': False,
                        'company_registry': False,
                        'parent_id': False,
                    })

                if not current_user:
                    current_user = request.env['res.users'].sudo().create({
                        'company_ids': [[6, False, [current_company.id]]],
                        'company_id': current_company.id,
                        'active': True,
                        'lang': 'en_US',
                        'tz': 'Europe/Brussels',
                        'image_1920': False,
                        '__last_update': False,
                        'name': kwargs['shop'],
                        'email': data['associated_user']['email'],
                        'login': kwargs['shop'],
                        'password': password_generate,
                        'action_id': False,
                    })
                vals['user'] = current_user.id
                vals['password'] = password_generate
                store_exist = request.env['shop'].sudo().search([('shop_url', '=', shop_url)], limit=1)
                if store_exist:
                    store_exist.write(vals)
                else:
                    store_exist = request.env['shop'].sudo().create(vals)

                print(current_user.password)
                return werkzeug.utils.redirect(base_url + '/bought-together')

                # except Exception as e:
                #     print(e)
        else:
            return json.dumps({"error": "No code in response"})

    @http.route('/bought-together/sync/product', type="http", auth="user", website=True, method=['GET'],
                csrf=False)
    def get_product(self, **kwargs):
        shop_url = request.session['shop_url']
        if shop_url:
            store_info = request.env['shop'].sudo().search([('shop_url', '=', shop_url)], limit=1)
        if self.sync_product():
            products = json.loads(self.sync_product())
        else:
            return json.dumps({
                "error": "Exception error"
            })
        if products:
            list_products = []
            for product in products['products']:
                vals = {}

                product_exist = request.env['shopify.product'].sudo().search([('product_id', '=', str(product['id']))],
                                                                        limit=1)
                vals['product_id'] = product['id']
                vals['store_id'] = store_info.id
                vals['name'] = product['title']
                vals['price'] = product['variants'][0]['price']
                vals['variant_id'] = product['variants'][0]['id']
                vals['image_url'] = product['image']['src']
                vals['compare_at_price'] = product['variants'][0]['compare_at_price']
                vals['qty_in_stock'] = product['variants'][0]['inventory_quantity']
                if product_exist:
                    product_exist.sudo().write(vals)
                else:
                    product_exist.sudo().create(vals)
                list_products.append(vals)
            return json.dumps({"products": list_products,
                               "shop_url": shop_url})
        else:
            return False

    def sync_product(self, params={}):

        shop_url = request.session['shop_url']
        store_info = request.env['shop'].sudo().search([('shop_url', '=', shop_url)], limit=1)
        if store_info:
            access_token = store_info.access_token
            header = {
                'X-Shopify-Access-Token': access_token,
            }
            response = requests.get("https://" + shop_url + '/admin/api/2023-01/products.json', headers=header,
                                    params=params)
            if response.ok:
                return json.dumps(response.json())
            else:
                return False
        else:
            return False

    @http.route('/bought-together/save/product', type="http", auth="user", website=True, method=['GET'],
                csrf=False)
    def save_product(self, **kwargs):
        print('haha')

