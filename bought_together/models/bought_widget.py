from odoo import fields, api, models


class BoughtWidget(models.Model):
    _name = 'bought.widget'
    store_id = fields.Many2one('shop')
    title = fields.Char()
    title_color = fields.Char()
    title_font_size = fields.Selection([('extra small', 'Extra Small'),
                                        ('small', 'Small'),
                                        ('medium', 'Medium'),
                                        ('large', 'Large'),
                                        ('extra large', 'Extra Large')],
                                       default='medium')
    description = fields.Char()
    description_color = fields.Char()
    description_font_size = fields.Selection([('extra small', 'Extra Small'),
                                              ('small', 'Small'),
                                              ('medium', 'Medium'),
                                              ('large', 'Large'),
                                              ('extra large', 'Extra Large')],
                                             default='medium')
    button_text = fields.Char()
    button_text_color = fields.Char()
    button_bg_color = fields.Char()
    button_border_color = fields.Char()
    total_price = fields.Char()
    product_included = fields.Float()
    product_recommend = fields.One2many('shopify.product', 'widget_recommend')
    product_exclude = fields.One2many('shopify.product', 'widget_exclude')
