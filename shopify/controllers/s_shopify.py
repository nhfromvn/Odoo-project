import json
from odoo import http
from odoo.http import request
import hmac
import hashlib
import requests
import werkzeug
import os
import jinja2
from pytz import timezone
from datetime import datetime

path = os.path.realpath(os.path.join(os.path.dirname(__file__), '../static/src/html'))
loader = jinja2.FileSystemLoader(path)
jinja_env = jinja2.Environment(loader=loader, autoescape=True)
jinja_env.filters["json"] = json.dumps

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


class SShopify(http.Controller):
    @http.route('/shopify', auth='user')
    def sc_index(self, **kw):
        template = jinja_env.get_template('index.html')
        res = template.render()
        return res

    @http.route('/shopify/api/app-settings', type="http", auth="public", website=True, method=['GET'], csrf=False)
    def app_settings(self, **kw):
        print("hello")

    @http.route('/shopify/install_app', type="http", auth="public", website=True, method=['GET'], csrf=False)
    def install_app(self, **kwargs):
        print(kwargs)
        shop_url = kwargs['shop']
        api_key = request.env['ir.config_parameter'].sudo().get_param('shopify.api_key')
        state = kwargs['hmac']
        callback = request.env['ir.config_parameter'].sudo().get_param('web.base.url') + '/shopify/oauth/callback'

        url = f"https://{shop_url}/admin/oauth/authorize?client_id={api_key}&scope={SCOPES}&redirect_uri={callback}&state={state}&grant_options[]=per-user"
        return werkzeug.utils.redirect(url)

    @http.route('/shopify/oauth/callback', type="http", auth="public", website=True, method=['GET'], csrf=False)
    def callback(self, **kwargs):
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
                store_exist = request.env['s.store.info'].sudo().search([('shop_url', '=', shop_url)], limit=1)
                if store_exist:
                    store_exist.write(vals)
                else:
                    store_exist = request.env['s.store.info'].sudo().create(vals)

                return werkzeug.utils.redirect(base_url + '/shopify')
                # except Exception as e:
                #     print(e)
        else:
            return json.dumps({"error": "No code in response"})

    @http.route('/shopify/order/list', type="http", auth="public", method=['GET'], csrf=False)
    def order_list(self):
        shop_url = request.session['shop_url']
        store_info = request.env['s.store.info'].sudo().search([('shop_url', '=', shop_url)], limit=1)

        if store_info:
            self.get_orders(store_info)
            result = {}
            vals_order = []
            for rec in store_info.sale_order_ids:
                items = []
                for item in rec.item_ids:
                    items.append({
                        "id_item": item.id_item,
                        "quantity": item.quantity,
                        "price": item.price,
                    })
                vals_order.append({
                    "id": rec.id_order,
                    "name": rec.name,
                    "item_lines": items,
                    "state": rec.state,
                    "financial_status": rec.financial_status,
                    # "total_price": rec.total_price
                })
            result['status'] = "success"
            result['orders'] = vals_order
            return json.dumps(result)
        else:
            return json.dumps({
                "error": "Not found store"
            })

    @http.route('/shopify/register-webhook', type="json", auth="public", website=True, method=['GET'], csrf=False)
    def register_webhook(self, topic, **kwargs):
        try:
            shop_url = request.session['shop_url']

            store_info = request.env['s.store.info'].sudo().search([('shop_url', '=', shop_url)], limit=1)
            if store_info:
                access_token = store_info.access_token
            else:
                return json.dumps({
                    "status": "error",
                    "message": "store not found"
                })

            doamin = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
            headers = {
                'X-Shopify-Access-Token': access_token,
                'Content-Type': 'application/json'
            }
            payload = {
                "webhook": {
                    "topic": topic,
                    "address": doamin + '/shopify/webhook/order',
                    "format": "json"
                }
            }
            try:
                response = requests.post("https://" + shop_url + "/admin/api/2023-01/webhooks.json",
                                         data=json.dumps(payload), headers=headers)
                if response.status_code == 200:
                    return response.json()
                else:
                    return {
                        "status": "error",
                        "status": response.json()
                    }
            except Exception as e:
                print(e)
        except Exception as e:
            print(e)

    # @http.route('/shopify/sync/order', type="http", auth="public", method=['POST'], csrf=False)
    # def sync_order(self, id_order, company, **kwargs):
    #     order = request.env['s.store.orders'].sudo().search([('id_order', '=', id_order)], limit=1)
    #     if order:
    #         data = {"Invoices": [{"Type": "ACCREC", "LineItems": [
    #             {"Description": "A Tires", "Quantity": 2, "UnitAmount": 20, "AccountCode": "200", "TaxType": "NONE",
    #              "LineAmount": 40}], "Date": "2019-03-11", "DueDate": "2018-12-10", "Reference": "Website Design",
    #                               "Status": "AUTHORISED"}]}

    @http.route('/shopify/webhook/list', type="json", auth="public", website=True, method=['GET', 'POST'],
                csrf=False)
    def webhook_list(self, **kwargs):

        try:
            shop_url = request.session['shop_url']
            store_info = request.env['s.store.info'].sudo().search([('shop_url', '=', shop_url)], limit=1)
            if store_info:
                access_token = store_info.access_token
                headers = {
                    'X-Shopify-Access-Token': access_token,
                }
                response = requests.get("https://" + shop_url + "/admin/api/2023-01/webhooks.json", headers=headers)
                return response.json()
            else:
                return json.dumps({
                    "status": "error",
                    "message": "store not found"
                })
        except Exception as e:
            print(e)

    @http.route('/shopify/webhook/delete', type="http", auth="public", website=True, method=['GET'],
                csrf=False)
    def webhook_delete(self, id_webhook, **kwargs):
        try:
            shop_url = request.session['shop_url']
            if shop_url:
                store_info = request.env['s.store.info'].sudo().search([('shop_url', '=', shop_url)], limit=1)
            if store_info:
                access_token = store_info.access_token
                headers = {
                    'X-Shopify-Access-Token': access_token,
                }
                enpoint = f"/admin/api/2023-01/webhooks/{id_webhook}.json"
                response = requests.delete("https://" + shop_url + enpoint, headers=headers)
                if response.status_code == 200:
                    return json.dumps({
                        "status": "success"
                    })
            else:
                return json.dumps({
                    "status": "error",
                    "message": "store not found"
                })
        except Exception as e:
            print(e)

    @http.route('/shopify/price_rules/list', type="json", auth="public", website=True, method=['GET', 'POST'],
                csrf=False)
    def price_rules_list(self, **kwargs):
        shop_url = request.session['shop_url']
        store_info = request.env['s.store.info'].sudo().search([('shop_url', '=', shop_url)], limit=1)
        if store_info:
            access_token = store_info.access_token
            headers = {
                'X-Shopify-Access-Token': access_token,
            }
            response = requests.get("https://" + shop_url + '/admin/api/2021-10/price_rules.json', headers=headers)

            return response.json()

    @http.route('/shopify/api/fetch-order', type="http", auth="public", website=True, method=['GET'], csrf=False)
    def api_fetch_order(self, **kwargs):
        shop_url = request.session['shop_url']
        store_info = request.env['s.store.info'].sudo().search([('shop_url', '=', shop_url)], limit=1)
        if store_info:
            access_token = store_info.access_token
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
                response = requests.get("https://" + shop_url + '/admin/api/2023-01/orders.json?status=any',
                                        headers=headers,
                                        params=params)
                if response.ok:
                    return json.dumps(response.json())

    @http.route('/shopify/api/fetch-product', type="http", auth="public", website=True, method=['GET'], csrf=False)
    def api_fetch_product(self, **kwargs):
        shop_url = request.session['shop_url']
        store_info = request.env['s.store.info'].sudo().search([('shop_url', '=', shop_url)], limit=1)
        if store_info:
            access_token = store_info.access_token
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
                if response.ok:
                    return json.dumps(response.json())

    @http.route('/shopify/webhook/order', type="http", auth="public", website=True, method=['GET'], csrf=False)
    def webhook_order(self, **kwargs):
        print(kwargs)

    @http.route('/shopify/webhook/product', type="http", auth="public", website=True, method=['GET', 'POST'],
                csrf=False)
    def webhook_product(self, **kwargs):
        print(kwargs)
    @http.route('/shopify/sync/product', type="http", auth="public", website=True, method=['GET'],
                csrf=False)
    def get_product(self, **kwargs):
        shop_url = request.session['shop_url']
        store_info = request.env['s.store.info'].sudo().search([('shop_url', '=', shop_url)], limit=1)
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

                product_exist = request.env['s.products'].sudo().search([('product_id', '=', str(product['id']))],
                                                                        limit=1)
                vals['product_id'] = product['id']
                vals['store_id'] = store_info.id
                vals['name'] = product['title']
                vals['price'] = product['variants'][0]['price']
                list_products.append(vals)
                if product_exist:
                    product_exist.sudo().write(vals)
                else:
                    product_exist.sudo().create(vals)

            return json.dumps({"products": list_products})
        else:
            return False

    def sync_product(self, params={}):

        shop_url = request.session['shop_url']
        store_info = request.env['s.store.info'].sudo().search([('shop_url', '=', shop_url)], limit=1)
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

    def get_orders(self, store):
        enpoint = 'https://' + store.shop_url + '/admin/api/2023-01/orders.json?status=any'
        headers = {
            "X-Shopify-Access-Token": store.access_token
        }
        res = requests.get(enpoint, headers=headers)

        if res.ok:
            data = res.json()
            for rec in data['orders']:
                vals_order = {}
                vals_item = {}
                order = request.env['s.store.orders'].sudo().search([('id_order', '=', rec['id'])], limit=1)
                vals_order['id_order'] = rec['id']
                vals_order['name'] = rec['name']
                vals_order['financial_status'] = rec['financial_status']
                # vals_order['total_price'] = rec['total_price']
                vals_order['s_store_id'] = store.id
                if order:
                    order.write(vals_order)
                else:
                    order = order.create(vals_order)
                for item in rec['line_items']:
                    item_exist = request.env['s.item.lines'].sudo().search(
                        [('product_id', '=', item['product_id'])],
                        limit=1)
                    vals_item['id_item'] = item['id']
                    vals_item['name'] = item['name']
                    vals_item['product_id'] = item['product_id']
                    vals_item['price'] = item['price']
                    vals_item['quantity'] = item['quantity']
                    vals_item['order_id'] = order.id
                    if item_exist:
                        item_exist.write(vals_item)
                    else:
                        item_exist.create(vals_item)

    @http.route('/shopify/cart/list', type="http", auth="public", website=True, method=['POST'], csrf=False)
    def get_cart(self, **kw):
        if request.httprequest.data:
            data = json.loads(request.httprequest.data)
            shop_url = data['shop_url']
            store_info = request.env['s.store.info'].sudo().search([('shop_url', '=', shop_url)], limit=1)
            list_price_discount = []
            item_ids = []
            combos_valid = []
            for item in data['items']:
                item_ids.append(str(item['product_id']))
            print(item_ids)
            # find valid combo
            for combo in store_info.combo_ids:
                if combo.product_lines:
                    for product in combo.product_lines:
                        print(str(product.product_id.product_id))
                        if str(product.product_id.product_id) in item_ids:
                            for item in data['items']:
                                if str(product.product_id.product_id) == str(item['product_id']):
                                    if item['quantity'] >= product.quantity:
                                        if combo not in combos_valid:
                                            combos_valid.append(combo)
                    for product in combo.product_lines:
                        if str(product.product_id.product_id) not in item_ids:
                            if combo in combos_valid:
                                combos_valid.remove(combo)
                            for item in data['items']:
                                if str(product.product_id.product_id) == str(item['product_id']):
                                    if item['quantity'] < product.quantity:
                                        if combo in combos_valid:
                                            combos_valid.remove(combo)
            # compute price
            for combo in combos_valid:
                original_total_price = data['original_total_price'] / 100
                list2 = []
                for item in data['items']:
                    for product in combo.product_lines:
                        if str(product.product_id.product_id) == str(item["product_id"]):
                            list2.append(item['quantity'] // product.quantity)
                amount_bundle = min(list2)
                for item in data['items']:
                    for product in combo.product_lines:
                        if str(product.product_id.product_id) == str(item["product_id"]):
                            item['qty_in_bundle'] = product.quantity * amount_bundle
                            item['qty_not_in_bundle'] = item['quantity'] - item['qty_in_bundle']
                total_price = 0
                total_not_in_bundle_price1 = 0
                for item in data['items']:
                    total_not_in_bundle_price1 += item['original_price'] * item['qty_not_in_bundle']
                total_not_in_bundle_price2 = 0
                product_ids = []
                for product in combo.product_lines:
                    product_ids.append(product.product_id.product_id)
                for item in data['items']:
                    if str(item['product_id']) not in product_ids:
                        print(combo.product_lines.product_id)
                        total_not_in_bundle_price2 = + item['original_price'] * item['quantity']
                total_price = total_not_in_bundle_price1 + total_not_in_bundle_price2 + combo.total_price * \
                              amount_bundle

                print("combo: " + str(combo.total_price))
                print("sprice:" + str(combo.subtotal_price))
                print("price:" + str(total_price))
                list_price_discount.append({
                    'price_discount': round(((combo.subtotal_price - combo.total_price) * amount_bundle), 1),
                    'total_price': total_price,
                    'combo_name': combo.name
                })
            best_discount = sorted(list_price_discount, key=lambda k: k['total_price'])[0]
            return json.dumps({
                "status": True,
                "best_discount": best_discount
            })
        else:
            return json.dumps({
                "status": False
            })

    # def get_cart(self, **kw):
    #     print(request.httprequest.data)
    #     if request.httprequest.data:
    #         data = json.loads(request.httprequest.data)
    #         shop_url = data['shop_url']
    #         store_info = request.env['s.store.info'].sudo().search([('shop_url', '=', shop_url)], limit=1)
    #         list_price_discount = []
    #         for combo in store_info.combo_ids:
    #             original_total_price = data['original_total_price'] / 100
    #             for item in data['items']:
    #                 price_discount = 0
    #                 if str(item['product_id']) == combo.product_condition.product_id:
    #                     if item['quantity'] >= combo.quantity_condition:
    #                         if combo.is_percent:
    #                             item_price = (item['price'] * item['quantity']) / 100
    #                             price_discount = combo.value * item_price / 100
    #
    #                         else:
    #                             if combo.type_apply:
    #                                 item_price = (item['price'] * item['quantity']) / 100
    #                                 price_discount = item_price - combo.value
    #                                 if price_discount <= 0:
    #                                     price_discount = item_price
    #                             else:
    #                                 price_discount = combo.value
    #                 original_total_price -= price_discount
    #             if original_total_price < 0:
    #                 original_total_price = 0
    #
    #             list_price_discount.append({
    #                 "combo": {
    #                     "id": combo.id,
    #                     "name": combo.name
    #                 },
    #                 "total_price_discount": original_total_price
    #             })
    #             print(list_price_discount)
    #         best_discount = sorted(list_price_discount, key=lambda k: k['total_price_discount'])[0]
    #         return json.dumps({
    #             "status": True,
    #             "price_discount": best_discount
    #         })
    #     else:
    #         return json.dumps({
    #             "status": False
    #         })

    @http.route('/shopify/register_script-tags', type="http", auth="public", website=True, csrf=False)
    def register_script_tags(self, **kw):

        shop_url = request.session['shop_url']
        store_info = request.env['s.store.info'].sudo().search([('shop_url', '=', shop_url)], limit=1)
        if store_info:
            try:
                header = {
                    'X-Shopify-Access-Token': store_info.access_token,
                    'Content-Type': 'application/json'
                }
                req = requests.post(f"https://{shop_url}/admin/api/2023-01/script_tags.json", headers=header,
                                    json={"script_tag": {"event": "onload",
                                                         "src": request.env['ir.config_parameter'].sudo().get_param(
                                                             'web.base.url') + "/shopify/static/src/js/scriptag.js"}})
                print(req.json())
            except Exception as e:
                print(e)

            return "hello"

    @http.route('/shopify/combo/list', type="http", auth="public", website=True, method=['GET'], csrf=False)
    def get_combo(self, **kw):
        if request.httprequest.data:
            shop_url = request.httprequest.data.decode('ascii')
        else:
            shop_url = request.session['shop_url']
        store_info = request.env['s.store.info'].sudo().search([('shop_url', '=', shop_url)], limit=1)
        if store_info:
            combo = request.env['s.combo'].sudo().search([('store_id', '=', store_info.id)])
            result = []
            if combo:
                for rec in combo:
                    vals = {}
                    vals['id'] = rec.id
                    vals['name'] = rec.name
                    vals['value'] = rec.value
                    vals['product_condition'] = {
                        'product_id': rec.product_condition.product_id,
                        'name': rec.product_condition.name,
                        'price': rec.product_condition.price,
                    }
                    vals['product_lines'] = []
                    for product in rec.product_lines:
                        vals['product_lines'].append({
                            "product": {
                                "product_id": product.product_id.product_id,
                                "name": product.product_id.name,
                                "price": product.product_id.price,
                                "store_id": rec.store_id.id
                            },
                            "quantity": product.quantity,
                            "discount_value": product.discount
                        })
                    vals['color'] = rec.color
                    vals['position'] = rec.position
                    if rec.is_percent:
                        vals['is_percent'] = True
                    else:
                        vals['is_percent'] = False
                    vals['type_apply'] = rec.type_apply
                    vals['quantity_condition'] = rec.quantity_condition
                    result.append(vals)
                return json.dumps(result)

    @http.route('/shopify/combo/update', type="json", auth="public", website=True, method=['POST'], csrf=False)
    def post_cart(self, **kw):
        if request.httprequest.data:
            res = json.loads(request.httprequest.data)
            data = res['value']
            shop_url = request.session['shop_url']
            vals = {}
            vals['name'] = data['name']
            vals['quantity_condition'] = data['quantity_condition']
            vals['value'] = data['value']
            vals['is_percent'] = data['is_percent']
            vals['type_apply'] = data['type_apply']
            combo_exist = request.env['s.combo'].sudo().search([('id', '=', data['id'])], limit=1)
            store_info = request.env['s.store.info'].sudo().search([('shop_url', '=', shop_url)], limit=1)
            if combo_exist:
                combo_exist.write(vals)
                for line in data["product_lines"]:
                    product = request.env['s.products'].sudo().search(
                        [('product_id', '=', line['product']['product_id'])],
                        limit=1)
                    line_exist = request.env['s.combo.products'].sudo().search(
                        ['&', ('product_id', '=', product.id), ('combo_id', '=', combo_exist.id)],
                        limit=1)
                    if line_exist:
                        line_exist.write({
                            'quantity': line['quantity'],
                            'discount': line['discount_value']
                        })
                    else:
                        request.env['s.combo.products'].sudo().create({
                            'product_id': product.id,
                            'combo_id': combo_exist.id,
                            'quantity': line['quantity'],
                            'discount': line['discount_value']
                        })
            else:
                vals['store_id'] = store_info.id
                combo = combo_exist.create(vals)
                for line in data["product_lines"]:
                    product = request.env['s.products'].sudo().search(
                        [('product_id', '=', line['product']['product_id'])],
                        limit=1)
                    request.env['s.combo.products'].sudo().create({
                        'product_id': product.id,
                        'combo_id': combo.id,
                        'quantity': line['quantity'],
                        'discount': line['discount_value']
                    })
            return {
                "status": True
            }

    # @http.route('/shopify/combo/update_line', type="json", auth="public", website=True, method=['POST'], csrf=False)
    # def post_line(self, **kw):
    #     if request.httprequest.data:
    #         res = json.loads(request.httprequest.data)
    #         shop_url = request.session['shop_url']
    #         line_exist = request.env['s.combo.products'].sudo().search([('product_id', '=', data['id'])], limit=1)
    #         store_info = request.env['s.store.info'].sudo().search([('shop_url', '=', shop_url)], limit=1)
    #         if combo_exist:
    #             combo_exist.write(vals)
    #         else:
    #             vals['store_id'] = store_info.id
    #             combo = combo_exist.create(vals)
    #         return {
    #             "status": True
    #         }

    @http.route('/shopify/combo/unlink', type="json", auth="public", website=True, method=['POST'], csrf=False)
    def unlink_combo(self):
        if request.httprequest.data:
            res = json.loads(request.httprequest.data)
            combo_exist = request.env['s.combo'].sudo().search([('id', '=', res['id'])], limit=1)
            if combo_exist:
                combo_exist.unlink()
                return {
                    "status": True
                }
            else:
                return {
                    "status": False
                }

    @http.route('/shopify/combo/apply', type="http", auth="public", website=True, method=['POST'], csrf=False)
    def apply_combo(self):
        if request.httprequest.data:
            res = json.loads(request.httprequest.data)
            shop = res['shop_url']
            combo = res['price_discount']['combo']['id']
            report = request.env['s.combo.report'].sudo().search([('combo_id', '=', combo)], limit=1)
            store_info = request.env['s.store.info'].sudo().search([('shop_url', '=', shop)], limit=1)

            vals = {}
            if report:
                report.applied += 1
            else:
                vals['combo_id'] = combo
                vals['store_id'] = store_info.id
                vals['applied'] = 1
                report.create(vals)
            return json.dumps({
                "status": True
            })

    @http.route('/shopify/combo/report', type="http", auth="public", website=True, method=['GET'], csrf=False)
    def combo_report(self):
        shop = request.session['shop_url']
        store_exist = request.env['s.store.info'].sudo().search([('shop_url', '=', shop)], limit=1)
        if store_exist:
            report = request.env['s.combo.report'].sudo().search([('store_id', '=', store_exist.id)])

            list_vals = []
            for rec in report:
                list_vals.append({
                    'id': rec.id,
                    'combo_name': rec.combo_id.name,
                    'total_apply': rec.applied,
                })
            return json.dumps({
                'report': list_vals
            })
