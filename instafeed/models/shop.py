from odoo import fields, api, models


class Shop(models.Model):
    _inherit = 'shop'
    instagram_access_token = fields.Char()
