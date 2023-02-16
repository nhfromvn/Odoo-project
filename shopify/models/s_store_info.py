from base64 import b64encode

import werkzeug.utils
from xero import Xero
from xero.constants import XeroScopes
from odoo import fields, models, api
import requests
from datetime import datetime
from urllib.parse import urlencode


class SStoreInfo(models.Model):
    _name = 's.store.info'
    _rec_name = 'shop_url'

    first_name = fields.Char(string="First name")
    last_name = fields.Char(string="Last name")
    shop_url = fields.Char(string="Shop")
    email = fields.Char(string="Email")
    locale = fields.Char(string="Locale")
    access_token = fields.Char(string="Shopify access token")
    code = fields.Char(string="Shopify code")
    xero_access_token = fields.Char(string="Xero access token")
    xero_refresh_token = fields.Char(string="Xero access token")
    state = fields.Selection([('disconnected', 'Disconnected'), ('connected', 'Connected')],
                             compute='_check_connect_xero')
    sale_order_ids = fields.One2many("s.store.orders", "s_store_id")
    combo_ids = fields.One2many("s.combo", "store_id")
    access_token_time_out = fields.Datetime()

    def _compute_time_out(self):
        # print(self.access_token_time_out)
        # print(datetime.now())
        # print(type(self.access_token_time_out))
        # print(type(datetime.now))
        access_token_time_out = datetime.now()

    def _check_connect_xero(self):
        for rec in self:
            if rec.xero_access_token:
                rec.state = 'connected'
            else:
                rec.state = 'disconnected'

    def connect_xero(self):

        client_id = self.env['ir.config_parameter'].sudo().get_param('xero.api_key')
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        shop_url = self.shop_url
        scope = " ".join([
            XeroScopes.OFFLINE_ACCESS,
            XeroScopes.ACCOUNTING_CONTACTS_READ,
            XeroScopes.ACCOUNTING_CONTACTS,
            XeroScopes.ACCOUNTING_TRANSACTIONS_READ,
            XeroScopes.ACCOUNTING_TRANSACTIONS,
            XeroScopes.ACCOUNTING_SETTINGS_READ,
            XeroScopes.ACCOUNTING_SETTINGS
        ])

        url = f'https://login.xero.com/identity/connect/authorize?response_type=code&client_id={client_id}&redirect_uri={base_url}/xero/callBack&scope={scope}&state={shop_url}'
        print(url)
        return {
            'type': 'ir.actions.act_url',
            'url': url
        }

    def refresh_access_xero(self):
        self._compute_time_out()
        print(self.access_token_time_out)
        client_id = self.env['ir.config_parameter'].sudo().get_param('xero.api_key')
        client_secret = self.env['ir.config_parameter'].sudo().get_param('xero.secret_key')
        refresh_token = self.xero_refresh_token

        enpoint = 'https://identity.xero.com/connect/token'
        header = {
            "authorization": "Basic " + b64encode(str(client_id + ":" + client_secret).encode('ascii')).decode('utf-8'),
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "grant_type": "refresh_token",
            "client_id": self.env['ir.config_parameter'].sudo().get_param('xero.api_key'),
            "refresh_token": refresh_token,
        }
        data = urlencode(data)
        response = requests.post(enpoint, headers=header, data=data)
        print(response.content)
        if response.ok:
            vals = {}
            data = response.json()
            vals["xero_access_token"] = data["access_token"]
            vals["xero_refresh_token"] = data["refresh_token"]
            self.write(vals)
            print(response.json())
