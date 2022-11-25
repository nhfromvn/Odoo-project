from odoo import models, fields, api


class ProductBundleProduct(models.Model):
    _name = 'product.bundle.product'
    _inherits = {'product.product': 'product_id'}
    product_id = fields.Many2one(
                'product.product',
                ondelete='cascade')
    bundle_id = fields.Many2one('product.bundle', string="Bundle")
    name = fields.Char('Name')
    quantity = fields.Integer('Quantity')
    product_vendor = fields.Many2one('res.partner',string = "Product Vendor")
    variants = fields.One2many('product.bundle.variant','product')
    discount = fields.Integer()


class ProductBundleVariant(models.Model):
    _name = 'product.bundle.variant'
    _inherits = {'product.product': 'product_id'}
    product_id = fields.Many2one(
        'product.product',
        ondelete='cascade')
    product = fields.Many2one('product.bundle.product')
    name = fields.Text('Name')
    bundle_id = fields.Many2one('product.bundle', string="Bundle")
