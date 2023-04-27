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


class BoughtTogetherController(http.Controller):
    @http.route('/instafeed/install', auth='user')
    def install_instafeed(self, **kwargs):
        print(kwargs)
        shop_url = kwargs['shop']
        api_key = request.env['ir.config_parameter'].sudo().get_param('instafeed.api_key_instafeed')
        state = kwargs['hmac']
        callback = request.env['ir.config_parameter'].sudo().get_param(
            'web.base.url') + '/instafeed/oauth/callback'

        url = f"https://{shop_url}/admin/oauth/authorize?client_id={api_key}&scope={SCOPES}&redirect_uri={callback}&state={state}&grant_options[]=per-user"
        return werkzeug.utils.redirect(url)

    @http.route('/instafeed/oauth/callback', type="http", auth="public", website=True, method=['GET'], csrf=False)
    def instafeed_callback(self, **kwargs):
        if 'code' in kwargs:
            code = kwargs['code']

            if 'shop' in kwargs:
                shop_url = kwargs['shop']
            else:
                return json.dumps({
                    "error": "not found shop_url in response"
                })
            api_key = request.env['ir.config_parameter'].sudo().get_param('instafeed.api_key_instafeed')
            secret = request.env['ir.config_parameter'].sudo().get_param('instafeed.secret_key_instafeed')
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
                store_exist = request.env['shop'].sudo().search([('shop_url', '=', shop_url)], limit=1)
                if store_exist:
                    store_exist.write(vals)
                else:
                    store_exist = request.env['shop'].sudo().create(vals)
                instafeed_user = request.env['instafeed.user'].sudo().search([('store_id', '=', store_exist.id)],
                                                                             limit=1)
                if not instafeed_user:
                    feed_exist = request.env['instafeed.user'].sudo().create({'store_id': store_exist.id})
                return werkzeug.utils.redirect(base_url + '/instafeed')
            # except Exception as e:
            #     print(e)
        else:
            return json.dumps({"error": "No code in response"})
