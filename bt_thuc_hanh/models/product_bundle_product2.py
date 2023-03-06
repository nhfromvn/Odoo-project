from odoo import models, fields, api


class ProductBundleProduct2(models.Model):
    _inherit = 'product.product'
    bundle_id = fields.One2many('product.bundle', 'product2', string="Bundle")
    tier_quantity = fields.One2many('product.bundle.qty', 'product2')


