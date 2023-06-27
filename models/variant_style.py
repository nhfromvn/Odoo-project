from odoo import models, fields, api


class VariantStyle(models.Model):
    _name = 'variant.style'
    shop = fields.Many2one('shopify.shop')
    type = fields.Char(default='Square Swatch')
    selected_swatch_outer_border = fields.Char(default='#000000')
    selected_swatch_inner_border = fields.Char(default='#DDDDDD')
    selected_button_border = fields.Char(default='#292929')
    selected_button_swatch_border = fields.Char(default='#CFCFCF')
    selected_button_text_color = fields.Char(default='#FFFFFF')
    selected_button_background_color = fields.Char(default='#292929')
    animation = fields.Char(default='no effect')
