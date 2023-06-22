from odoo import models, fields, api


class Theme(models.Model):
    _name = 'shopify.theme'
    theme_id = fields.Char()
    shop = fields.Many2one('shopify.shop')
    is_active = fields.Boolean()
