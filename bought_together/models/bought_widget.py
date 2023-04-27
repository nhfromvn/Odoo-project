from odoo import fields, api, models


class BoughtWidget(models.Model):
    _name = 'bought.widget'
    store_id = fields.Many2one('shop')
    title = fields.Char(default="YOU MAY ALSO LIKE...")
    title_color = fields.Char(default='#000000')
    title_font_size = fields.Selection([('extra small', 'Extra Small'),
                                        ('small', 'Small'),
                                        ('medium', 'Medium'),
                                        ('large', 'Large'),
                                        ('extra large', 'Extra Large')],
                                       default='medium')
    description = fields.Char(default="Good deals only for you!")
    description_color = fields.Char(default='#000000')
    description_font_size = fields.Selection([('extra small', 'Extra Small'),
                                              ('small', 'Small'),
                                              ('medium', 'Medium'),
                                              ('large', 'Large'),
                                              ('extra large', 'Extra Large')],
                                             default='medium')
    button_text = fields.Char(default='Add to cart')
    button_text_color = fields.Char(default='#FFFFFF')
    button_bg_color = fields.Char(default='#000000')
    button_border_color = fields.Char(default='#000000')
    total_price = fields.Float()
    product_included = fields.Integer(compute='_compute_product')
    numbers_product = fields.Integer(default=3)
    product_recommend = fields.One2many('shopify.product', 'widget_recommend')
    product_exclude = fields.One2many('shopify.product', 'widget_exclude')
    status = fields.Boolean(default=True)

    @api.depends('product_recommend')
    def _compute_product(self):
        for widget in self:
            widget.product_included = len(widget.product_recommend)


class BoughtTogetherConfig(models.TransientModel):
    _inherit = 'res.config.settings'
    api_key_bought_together = fields.Char()
    secret_key_bought_together = fields.Char()

    @api.model
    def get_values(self):
        res = super().get_values()
        params = self.env['ir.config_parameter'].sudo()
        res.update(
            api_key_bought_together=str(params.get_param('bought_together.api_key_bought_together')),
            secret_key_bought_together=str(params.get_param('bought_together.secret_key_bought_together')))
        return res

    def set_values(self):
        super().set_values()
        param = self.env['ir.config_parameter'].sudo()

        field_api_key = self.api_key_bought_together if self.api_key_bought_together else False
        field_secret_key = self.secret_key_bought_together if self.secret_key_bought_together else False

        param.set_param('bought_together.api_key_bought_together', field_api_key)
        param.set_param('bought_together.secret_key_bought_together', field_secret_key)
