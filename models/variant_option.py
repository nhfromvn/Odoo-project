from odoo import models, fields, api


class VariantOption(models.Model):
    _name = 'variant.option'
    option_name = fields.Char()
    shop = fields.Many2one('shopify.shop')
    prevent_default = fields.Boolean(default=False)
    collection_page_swatch_image = fields.Char(default='Use 1st image of variant')
    product_page_swatch_image = fields.Char(default='Use 1st image of variant')
    product_style = fields.Many2one('variant.style')
    collection_style = fields.Many2one('variant.style')
    type = fields.Char(default='option_only')
    inventory_threshold = fields.Integer(default=10)
    notification_message = fields.Char(default='Only 10 left')
    option_label = fields.Char(default='Only 10 left')
    add_to_cart_label = fields.Char(default='Only 10 left')
    product_affected = fields.Integer(default=0)
