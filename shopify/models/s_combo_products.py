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
    variant_id = fields.Many2one('s.product.variants')
    variant_name = fields.Char(compute='compute_name')
    @api.depends('variant_id.variant_name')
    def compute_name(self):
        for line in self:
            # if line.variant_id.variant_name == 'Default Title':
            #     line.variant_name = ""
            # else:
            line.variant_name = line.variant_id.variant_name

    @api.depends('variant_id.price', 'combo_id.is_percent')
    def _compute_price(self):
        for product in self:
            if product.combo_id.is_percent:
                product.price = product.variant_id.price * (1 - product.discount / 100)
            else:
                product.price = product.variant_id.price - product.discount
