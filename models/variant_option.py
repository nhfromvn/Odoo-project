from odoo import models, fields, api


class VariantOption(models.Model):
    _name = 'variant.option'
    option_name = fields.Char()
    shop = fields.Many2one('shopify.shop')
    prevent_default = fields.Boolean(default=False)
    collection_page_swatch_style = fields.Char()
    collection_page_swatch_image = fields.Char()
    product_page_swatch_style = fields.Char()
    product_page_swatch_image = fields.Char()
    product_page_styles = fields.One2many('variant.style', 'variant_option_product')
    collection_page_styles = fields.One2many('variant.style', 'variant_option_collection')
    selected_product_page_style = fields.Char(default='Square swatch')
    selected_collection_page_style = fields.Char(default='Square swatch')
    type = fields.Char(default='option_only')
    inventory_threshold = fields.Integer(default=10)
    notification_message = fields.Char(default='auto')
    option_label = fields.Char()
    add_to_cart_label = fields.Char()
    product_affected = fields.Integer(default=0)
