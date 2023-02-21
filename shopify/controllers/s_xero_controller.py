import json
import werkzeug.utils
from odoo import http
from odoo.http import request
from base64 import b64encode
import requests
from datetime import datetime


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

                return werkzeug.utils.redirect(base_url + '/shopify')

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

    @http.route(['/xero/list-contact'], type='http', auth="public", website=True, method=['GET'], csrf=False)
    def list_contact(self, **kwargs):
        try:
            shop_url = request.session['shop_url']
            enpoint = 'https://api.xero.com/api.xro/2.0/Contacts'
            if shop_url:
                store_info = request.env['s.store.info'].sudo().search([('shop_url', '=', shop_url)], limit=1)
                if store_info:
                    header = {
                        "Xero-Tenant-Id": kwargs['tenant_id'],
                        "Authorization": "Bearer " + store_info.xero_access_token,
                        "Accept": "application/json"
                    }
                    response = requests.get(enpoint, headers=header)
                    data = json.loads(response.content)
                    if response.status_code != 404:
                        if response.ok:
                            return json.dumps({
                                "status": "success",
                                "result": data
                            })
                        else:
                            if 'Detail' in data:
                                if 'TokenExpired' in data['Detail']:
                                    store_info.refresh_access_xero()
                                    self.list_contact()
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

    @http.route(['/xero/list-account'], type='http', auth="public", website=True, method=['GET'], csrf=False)
    def list_account(self, **kwargs):
        try:
            shop_url = request.session['shop_url']
            enpoint = 'https://api.xero.com/api.xro/2.0/Accounts'
            if shop_url:
                store_info = request.env['s.store.info'].sudo().search([('shop_url', '=', shop_url)], limit=1)
                if store_info:
                    header = {
                        "Xero-Tenant-Id": kwargs['tenant_id'],
                        "Authorization": "Bearer " + store_info.xero_access_token,
                        "Accept": "application/json"
                    }
                    response = requests.get(enpoint, headers=header)
                    data = json.loads(response.content)
                    if response.status_code != 404:
                        if response.ok:
                            return json.dumps({
                                "status": "success",
                                "result": data
                            })
                        else:
                            if 'Detail' in data:
                                if 'TokenExpired' in data['Detail']:
                                    store_info.refresh_access_xero()
                                    self.list_account()
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

    @http.route(['/xero/sync-all-orders'], type='http', auth="public", website=True, method=['GET'], csrf=False)
    def sync_all(self, **kwargs):
        shop_url = request.session['shop_url']
        store_info = request.env['s.store.info'].sudo().search([('shop_url', '=', shop_url)], limit=1)
        orders = request.env['s.store.orders'].sudo().search([('s_store_id', '=', store_info.id)])
        header = {
            'Authorization': 'Bearer ' + str(store_info.xero_access_token),
            'Xero-Tenant-Id': kwargs['tenant_id'],
            'Accept': 'application/json',
        }
        invoices = []
        payments = []
        for order in orders:
            if order.state == 'yet_sync':
                items = []
                total_price = 0
                if order.item_ids:
                    for item in order.item_ids:
                        total_price += item.quantity * item.price
                        items.append({
                            "Description": "hello",
                            "Quantity": item.quantity,
                            "UnitAmount": item.price,
                            "AccountCode": "200",
                            "TaxType": "NONE",
                            "LineAmount": item.quantity * item.price,
                        })
                    invoices.append({
                        "Type": "ACCREC",
                        "Contact": {
                            "ContactID": kwargs['contact_id']
                        },
                        "LineItems": items,
                        "Date": "2019-03-11",
                        "DueDate": datetime.today().strftime("%Y-%m-%d"),
                        "Reference": "Website Design",
                        "Status": "AUTHORISED"
                    })
                    order.state = 'synced'
        if invoices:
            payload = {
                "Invoices": invoices
            }
            url = 'https://api.xero.com/api.xro/2.0/Invoices'
            response = requests.post(url, headers=header, json=payload)
            Invoices = response.json()
            if response.status_code != 404:
                if response.ok:
                    print(Invoices)
                else:
                    if 'Detail' in Invoices:
                        if 'TokenExpired' in Invoices['Detail']:
                            store_info.refresh_access_xero()
                            self.sync_order()
                            print('error')
                        else:
                            print('not found')
            else:
                print('error')
        else:
            return json.dumps({
                'status': "synced"
            })

    @http.route('/shopify/sync/order', type="http", auth="public", website=True, method=['GET', 'POST'],
                csrf=False)
    def sync_order(self, **kwargs):

        print(kwargs)
        shop_url = request.session['shop_url']
        store_info = request.env['s.store.info'].sudo().search([('shop_url', '=', shop_url)], limit=1)
        order = request.env['s.store.orders'].sudo().search([('id_order', '=', kwargs['order_id'])], limit=1)
        if order.state == 'yet_sync':
            print(order)
            header = {
                'Authorization': 'Bearer ' + str(store_info.xero_access_token),
                'Xero-Tenant-Id': kwargs['tenant_id'],
                'Accept': 'application/json',
            }

            items = []
            total_price = 0
            if order.item_ids:
                for item in order.item_ids:
                    total_price += item.quantity * item.price
                    items.append({
                        "Description": "hello",
                        "Quantity": item.quantity,
                        "UnitAmount": item.price,
                        "TaxType": "NONE",
                        "AccountCode": "200",
                        "LineAmount": item.quantity * item.price,
                    })
            else:
                return json.dumps({
                    "status": "line error"
                })
            payload = {
                "Invoices": [
                    {"Type": "ACCREC",
                     "Contact": {
                         "ContactID": kwargs['contact_id']
                     }, "LineItems": items,
                     "Date": "2019-03-11",
                     "DueDate": datetime.today().strftime("%Y-%m-%d"),
                     # "Reference": "Website Design",
                     "Status": "AUTHORISED"
                     }
                ]
            }
            url = 'https://api.xero.com/api.xro/2.0/Invoices'
            response = requests.post(url, headers=header, json=payload)
            invoices = response.json()
            print(invoices)
            if response.status_code != 404:
                if response.ok:
                    print(invoices)
                else:
                    if 'Detail' in invoices:
                        if 'TokenExpired' in invoices['Detail']:
                            store_info.refresh_access_xero()
                            self.sync_order()
                        else:
                            print('error')
            else:
                print('error')
            order.state = 'synced'
            if order.financial_status == "paid":
                payload2 = {
                    "Invoice": {"InvoiceID": invoices['Invoices'][0]['InvoiceID'],
                                "LineItems": items},
                    "Account": {"AccountID": kwargs["account_id"]},
                    "Date": datetime.today().strftime("%Y-%m-%d"),
                    "Amount": total_price
                }
                url = 'https://api.xero.com/api.xro/2.0/Payments'
                payments = requests.put(url, headers=header, json=payload2)
                print(payments.content)
                if payments.ok:
                    print('haha')
                    return json.dumps({
                        "status": "success"
                    })
                else:
                    return json.dumps({
                        "status": "payments error",
                        "result": payments.json()
                    })
            else:
                return json.dumps({
                    "status": "order error"
                })
        else:
            return json.dumps({
                "status": "synced"
            })
