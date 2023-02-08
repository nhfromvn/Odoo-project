import json

import werkzeug.utils

from odoo import http
from odoo.http import request
from base64 import b64encode
import requests


class SXeroController(http.Controller):

    @http.route(['/xero/callBack'], type="http", auth="public", website=True, method=['GET'], csrf=False)
    def xero_callback(self, **kwargs):
        print(kwargs)
        if 'code' in kwargs:
            endpoint = 'https://identity.xero.com/connect/token'
            client_id = request.env['ir.config_parameter'].sudo().get_param('xero.api_key')
            client_secret = request.env['ir.config_parameter'].sudo().get_param('xero.secret_key')
            code = kwargs['code']
            state = kwargs['state']
            base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')

            header = {
                "authorization": "Basic " + b64encode(str(client_id + ":" + client_secret).encode('ascii')).decode(
                    'utf-8'),
                "Content-Type": "application/x-www-form-urlencoded"
            }
            data = {
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": base_url + "/xero/callBack"
            }

            responce = requests.post(endpoint, headers=header, data=data)
            if responce.ok:
                data = responce.json()
                print(data)
                vals = {}
                if 'access_token' in data:
                    vals['xero_access_token'] = data['access_token']
                if 'refresh_token' in data:
                    vals['xero_refresh_token'] = data['refresh_token']
                store_exist = request.env['s.store.info'].sudo().search([('shop_url', '=', state)], limit=1)
                if store_exist:
                    store_exist.write(vals)

                return werkzeug.utils.redirect(base_url+'/shopify')

    @http.route(['/xero/check-connect'], type='json', auth="public", website=True, method=['GET'], csrf=False)
    def xero_check_connect(self, **kwargs):
        try:
            shop_url = request.session['shop_url']
            if shop_url:
                store_info = request.env['s.store.info'].sudo().search([('shop_url', '=', shop_url)], limit=1)
                if store_info:
                    if store_info.state == 'connected':
                        return {
                            "status": True
                        }
                    elif store_info.state == 'connected':
                        return {
                            "status": False
                        }
                    else:
                        return {
                            "error": "shop not found"
                        }
            else:
                return {
                    "error": "shop not found"
                }
        except Exception as e:
            print(e)

    @http.route(['/xero/list-connections'], type='http', auth="public", website=True, method=['GET'], csrf=False)
    def list_connection(self):
        try:
            shop_url = request.session['shop_url']
            enpoint = 'https://api.xero.com/connections'

            if shop_url:
                store_info = request.env['s.store.info'].sudo().search([('shop_url', '=', shop_url)], limit=1)
                if store_info:
                    header = {
                        "Authorization": "Bearer " + store_info.xero_access_token,
                        "Content-Type": "application/json"
                    }

                    response = requests.get(enpoint, headers=header)
                    if response.status_code != 404:
                        if response.ok:
                            return json.dumps({
                                "status": "success",
                                "result": response.json()
                            })
                        else:
                            data = response.json()
                            if 'Detail' in data:
                                if 'TokenExpired' in data['Detail']:
                                    store_info.refresh_access_xero()
                                    self.list_connection()
                                else:
                                    return json.dumps({
                                        "error": data
                                    })
                    else:
                        return json.dumps({
                            "error": "Not Found"
                        })
        except Exception as e:
            print(e)