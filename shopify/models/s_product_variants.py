from odoo import fields, models, api


class SProductVariants(models.Model):
    _name = 's.product.variants'
    price = fields.Float()
    product_id = fields.Many2one('s.products')
    variant_id = fields.Char()
    variant_name = fields.Char()
