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

    @http.route('/bought-together/save/product', type="json", auth="user", website=True, method=['POST'], csrf=False)
    def save_product(self, **kwargs):
        if request.httprequest.data:
            res = json.loads(request.httprequest.data)
            print(res)
            shop_url = res['shop_url']
            print(shop_url)
            vals = {}
            store_info = request.env['shop'].sudo().search([('shop_url', '=', shop_url)], limit=1)
            widget_exist = request.env['bought.widget'].sudo().search([('store_id', '=', store_info.id)],
                                                                      limit=1)
            print(widget_exist)
            vals['title'] = res['widget_title']
            vals['title_color'] = res['widget_title_color']
            vals['title_font_size'] = res['widget_title_font_size']
            vals['description'] = res['widget_description']
            vals['description_color'] = res['widget_description_color']
            vals['description_font_size'] = res['widget_description_font_size']
            vals['button_text'] = res['widget_button_text']
            vals['button_text_color'] = res['widget_button_text_color']
            vals['button_bg_color'] = res['widget_button_bg_color']
            vals['button_border_color'] = res['widget_button_border_color']
            vals['total_price'] = res['total_price']
            vals['numbers_product'] = res['numbers_product']
            if widget_exist:
                widget_exist.write(vals)
            else:
                vals['store_id'] = store_info.id
                widget_exist = request.env['bought.widget'].sudo().create(vals)
            for product_id in res['list_recommend_product_id']:
                shop_product = request.env['shopify.product'].sudo().search(
                    [('product_id', '=', str(product_id))],
                    limit=1)
                shop_product.write({'widget_recommend': widget_exist.id})
                if shop_product not in widget_exist.product_recommend:
                    widget_exist.write({'product_recommend': [(4, shop_product.id)]})
            for product_id in res['list_exclude_product_id']:
                shop_product = request.env['shopify.product'].sudo().search(
                    [('product_id', '=', str(product_id))],
                    limit=1)
                shop_product.write({'widget_exclude': widget_exist.id})
                if shop_product not in widget_exist.product_exclude:
                    widget_exist.write({'product_exclude': [(4, shop_product.id)]})
            for product in widget_exist.product_recommend:
                if int(product.product_id) not in res['list_recommend_product_id']:
                    widget_exist.write({'product_recommend': [(3, product.id)]})
            for product in widget_exist.product_exclude:
                if int(product.product_id) not in res['list_exclude_product_id']:
                    widget_exist.write({'product_exclude': [(3, product.id)]})
            return {
                "status": True
            }

    @http.route('/bought-together/get/widget', type="http", auth="user", website=True, method=['GET'],
                csrf=False)
    def get_widget(self):
        shop_url = request.session['shop_url']
        if shop_url:
            store_info = request.env['shop'].sudo().search([('shop_url', '=', shop_url)], limit=1)
        widget = request.env['bought.widget'].sudo().search([('store_id', '=', store_info.id)],
                                                            limit=1)
        vals = {}
        vals['widget_title'] = widget.title
        vals['widget_title_color'] = widget.title_color
        vals['widget_title_font_size'] = widget.title_font_size
        vals['widget_description'] = widget.description
        vals['widget_description_color'] = widget.description_color
        vals['widget_description_font_size'] = widget.description_font_size
        vals['widget_button_text'] = widget.button_text
        vals['widget_button_text_color'] = widget.button_text_color
        vals['widget_button_bg_color'] = widget.button_bg_color
        vals['widget_button_border_color'] = widget.button_border_color
        vals['numbers_product'] = widget.numbers_product
        vals['total_price'] = widget.total_price
        vals['product_included'] = widget.product_included
        vals['list_recommend_product'] = []
        vals['list_exclude_product'] = []
        for product in widget.product_recommend:
            vals['list_recommend_product'].append(str(product.product_id))
        for product in widget.product_exclude:
            vals['list_exclude_product'].append(str(product.product_id))
        return json.dumps(vals)
