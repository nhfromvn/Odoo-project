

from odoo import models, fields, api

class ShopifyApp(models.Model):
    _name = 'sp.app'
    _description = 'Shopify App'
    shop_url = fields.Char()
    name = fields.Char(index=True)
    sp_api_key = fields.Char()
    sp_api_secret_key = fields.Char()
    sp_api_version = fields.Char()
    gg_api_client_id = fields.Char()
    gg_api_client_secret = fields.Char()
    cdn_tag = fields.Char()
