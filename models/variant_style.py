from odoo import models, fields, api


class VariantStyle(models.Model):
    _name = 'variant.style'
    shop = fields.Many2one('shopify.shop')
    type = fields.Char(default='Square Swatch')
    selected_swatch_outer_border = fields.Char()
    selected_swatch_inner_border = fields.Char()
    selected_button_border = fields.Char()
    selected_button_swatch_border = fields.Char()
    selected_button_text_color = fields.Char()
    selected_button_background_color = fields.Char()
    animation = fields.Char()
    variant_option_collection = fields.Many2one('variant.option')
    variant_option_product = fields.Many2one('variant.option')
