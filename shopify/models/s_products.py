from odoo import fields, models, api


class SProducts(models.Model):
    _name = 's.products'
    _description = 'Products'
    _rec_name = 'name'
    product_id = fields.Char()
    store_id = fields.Many2one("s.store.info")
    name = fields.Char()
    price = fields.Float()
    variant_id = fields.Char()
    variants = fields.One2many('s.product.variants', 'product_id')
