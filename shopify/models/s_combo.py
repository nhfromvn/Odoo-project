from odoo import fields, models, api


class SProducts(models.Model):
    _name = 's.combo'
    _description = 'Combo'
    _rec_name = 'name'
    priority = fields.Integer()
    name = fields.Char()
    is_percent = fields.Boolean()
    value = fields.Float()
    type_apply = fields.Boolean(default=False)
    store_id = fields.Many2one("s.store.info")
    product_condition = fields.Many2one("s.products")
    product_lines = fields.One2many("s.combo.products", 'combo_id')
    quantity_condition = fields.Integer()
    color_ = fields.Char(default= "#DF1111")
    position = fields.Selection([('below', 'below cart'),
                                 ('above', 'above cart')],
                                'Position', default='below')
    total_price = fields.Float(compute="_compute_total")
    subtotal_price = fields.Float(compute="_compute_subtotal")
    @api.depends('product_lines.price', 'type_apply', 'is_percent')
    def _compute_total(self):
        for combo in self:
            if combo.type_apply:
                combo.total_price = 0
                for product in combo.product_lines:
                    combo.total_price += product.price * product.quantity
            else:
                if combo.is_percent:
                    combo.total_price = combo.subtotal_price * (1 - combo.value / 100)
                else:
                    combo.total_price = combo.subtotal_price - combo.value

    @api.depends('product_lines.product_id.price')
    def _compute_subtotal(self):
        for combo in self:
            combo.subtotal_price = 0
            for product in combo.product_lines:
                combo.subtotal_price += product.product_id.price * product.quantity
