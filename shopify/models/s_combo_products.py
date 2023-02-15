from odoo import fields, models, api


class SComboProducts(models.Model):
    _name = 's.combo.products'
    combo_id = fields.Many2one('s.combo')
    quantity = fields.Integer()
    discount = fields.Float()
    product_id = fields.Many2one('s.products')
    price = fields.Float(compute='_compute_price')
    qty_in_bundle = fields.Integer()
    qty_not_in_bundle = fields.Integer()

    @api.depends('product_id.price', 'combo_id.is_percent')
    def _compute_price(self):
        for product in self:
            if product.combo_id.is_percent:
                product.price = product.product_id.price * (1 - product.discount / 100)
            else:
                product.price = product.product_id.price - product.discount
