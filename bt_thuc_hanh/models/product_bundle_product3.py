from odoo import models, fields, api


class ProductBundleProduct3(models.Model):
    _name = 'product.bundle.product3'
    _inherits = {'product.product': 'product_id'}

    product_id = fields.Many2one(
        'product.product',
        ondelete='cascade')
    bundle_id = fields.Many2one('product.bundle', string="Bundle")
    name = fields.Char('Name')
