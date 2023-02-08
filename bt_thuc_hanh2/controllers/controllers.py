import json
from odoo import http
from odoo.http import request
import requests
import werkzeug
import shopify
import random
import json
import string
from datetime import datetime

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


class BtThucHanh2(http.Controller):
    @http.route('/shopify/install1', auth='public', type="http", website=True, method=['GET'], csrf=False)
    def index(self, **kw):
        print(kw)
        shop_url = kw['shop']
        state = kw['hmac']
        callback = request.env['ir.config_parameter'].sudo().get_param('web.base.url') + '/bt_shopify/oauth/callback1'
        url = f"https://{shop_url}/admin/oauth/authorize?client_id={'1754cae9ec7a77b1c13ebf973ebd0d9c'}&scope={SCOPES}&redirect_uri={callback}&state={state}&grant_options[]=per-user"
        return werkzeug.utils.redirect(url)

    @http.route('/shopify/oauth/callback1', auth='public', type="http", website=True, method=['GET'], csrf=False)
    def shopify(self, **kw):
        check = 0
        print(kw)
        shop_url = kw['shop']
        apps = request.env['sp.app'].search([])
        current_app = apps[0]
        if 'shop' in kw:
            try:
                shopify.Session.setup(
                    api_key=current_app.sp_api_key,
                    secret=current_app.sp_api_secret_key)
                shopify_session = shopify.Session(kw['shop'], current_app.sp_api_version)
                token = shopify_session.request_token(kw)
                shopify.ShopifyResource.activate_session(shopify_session)
                if token:
                    print('token: ' + token)
                    shopify.ShopifyResource.activate_session(shopify_session)
                    shop = shopify.Shop.current()  # Get the current shop
                    sp_shops = request.env['sp.shop'].search([])
                    for sp_shop in sp_shops:
                        if sp_shop.shop_url == shop_url:
                            sp_shop.token = token
                            check = 1
                            break
                        else:
                            check = 0
                    if not check:
                        request.env['sp.shop'].sudo().create({
                            'name': shop_url,
                            'shop_url': shop_url,
                            'currency_code': shop.currency,
                            'country': shop.country,
                            'email': shop.email,
                            'token': token,
                            # 'password': shop.password
                        })
                    # execute a graphQL call
                    # bt_shopify.GraphQL().execute("{ shop { name id } }")

                shopify.ShopifyResource.clear_session()
            except Exception as ex:
                print(ex)
                return "eror"
            return "hello"

    @http.route('/shopify/register-webhook1', type="http", auth="public", website=True, csrf=False)
    def register(self):
        try:
            shop = request.env['sp.shop'].search([])[-1]
            print(shop.token)
            header = {
                'X-Shopify-Access-Token': shop.token,
                'Content-Type': 'application/json'
            }
            req = requests.post(f"https://{shop.shop_url}/admin/api/2023-01/webhooks.json", headers=header,
                                json={
                                    "webhook": {
                                        "topic": "products/create",
                                        "address": request.env['ir.config_parameter'].sudo().get_param(
                                            'web.base.url') + "/bt_shopify/webhook/products",
                                        "format": "json"
                                    }
                                })
            print(req.json())
        except Exception as e:
            print(e)
        return "hello"

    @http.route('/shopify/webhook/products', type='json', auth="public", csrf=False)
    def webhook_product(self, **kwargs):
        data = request.jsonrequest
        print(request)
        print(data)
        return {
            'status': 'success'
        }

    @http.route('/shopify/register-webhook/update', type="http", auth="public", website=True,
                csrf=False)
    def register_webhook(self):
        try:
            shop = request.env['sp.shop'].search([])[-1]
            print(shop.token)
            header = {
                'X-Shopify-Access-Token': shop.token,
                'Content-Type': 'application/json'
            }
            req = requests.post(f"https://{shop.shop_url}/admin/api/2023-01/webhooks.json", headers=header,
                                json={
                                    "webhook": {
                                        "topic": "products/update",
                                        "address": request.env['ir.config_parameter'].sudo().get_param(
                                            'web.base.url') + "/bt_shopify/webhook/products/update",
                                        "format": "json"
                                    }
                                })
            print(req.json())
        except Exception as e:
            print(e)
        return "hello"

    @http.route('/shopify/webhook/products/update', type='json', auth="public", csrf=False)
    def webhook_product_update(self, **kwargs):
        data = request.jsonrequest
        print(request)
        print(data)
        return {
            'status': 'success'
        }

    @http.route('/script-tags/create', type='http')
    def create_script_tag(self):
        try:
            shop = request.env['sp.shop'].search([])[-1]
            print(shop.token)
            header = {
                'X-Shopify-Access-Token': shop.token,
                'Content-Type': 'application/json'
            }
            req = requests.post(f"https://{shop.shop_url}/admin/api/2023-01/script_tags.json", headers=header,
                                json={"script_tag": {"event": "onload",
                                                     "src": request.env['ir.config_parameter'].sudo().get_param(
                                                         'web.base.url') + "/bt_thuc_hanh2/static/src/js/script_tag.js"}})
            print(req.json())
        except Exception as e:
            print(e)
        return "hello"

    @http.route('/shopify/api/fetch-product1', type="http", auth="public", website=True, method=['GET'], csrf=False)
    def api_fetch_product(self, **kwargs):
        store_info = request.env['sp.shop'].sudo().search([], limit=1)
        shop_url = store_info.shop_url
        if store_info:
            access_token = store_info.token
            headers = {
                'X-Shopify-Access-Token': access_token,
            }
            params = {}
            if 'start' in kwargs:
                start = int(kwargs['start']) / 1000
                start_time = datetime.fromtimestamp(start).date()
                params['published_at_min'] = str(start_time) + 'T00:00:00'
            if 'end' in kwargs:
                start = int(kwargs['end']) / 1000
                end_time = datetime.fromtimestamp(start).date()
                params['published_at_max'] = str(end_time) + 'T23:59:59'
            if len(params) > 0:
                print(params)
            response = requests.get("https://" + shop_url + '/admin/api/2021-10/products.json', headers=headers,
                                    params=params)
            products = request.env['sp.product'].search([])
            ids = []
            for product in products:
                if product.id not in ids:
                    ids.append(int(product.product_id))
            for product in response.json()['products']:
                if product['id'] not in ids:
                    request.env['sp.product'].sudo().create({
                        'product_id': product['id'],
                        # 'store_id': request.env['sp.shop'].search([('shop_url','=',str(product['vendor']+'.myshopify.com'))]),
                        'name': product['title'],
                        # 'password': shop.password
                    })
                else:
                    a = request.env['sp.product'].search([('product_id', '=', product['id'])])
                    a.price = product['variants'][0]['price']
                    a.store_id = request.env['sp.shop'].search([])[0]
            if response.ok:
                return "hello"
