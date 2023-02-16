from base64 import b64encode

import werkzeug.utils
from xero import Xero
from xero.constants import XeroScopes
from odoo import fields, models, api
import requests


class XeroInfo(models.Model):
    _name = 'xero.info'
    sales_account_code = fields.Char('Sales Account Code')
    payment_account_code = fields.Char('Payment Account Code')
    shipping_account_code = fields.Char('Shipping Account Code')
    date_start = fields.Date('Date Start')
    date_end = fields.Date('Date End')
