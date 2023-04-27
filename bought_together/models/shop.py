from odoo import fields, api, models


class Shop(models.Model):
    _name = 'shop'
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
    user = fields.Many2one('res.users')
    password = fields.Char()
    test = fields.Char()