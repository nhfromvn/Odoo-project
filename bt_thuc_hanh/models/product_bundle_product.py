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
    product_vendor = fields.Many2one('res.partner', string="Product Vendor")
    variants = fields.One2many('product.bundle.variant', 'product')
    discount = fields.Integer()
    list_price = fields.Float(compute='_compute_price')
    list_price_bundle = fields.Float()
    image = fields.Binary(attachment=True)
    bundle_date = fields.Date.today()

    @api.depends('product_id.list_price')
    def _compute_price(self):
        for product in self:
            if product.bundle_id.discount_rule == 'product':
                product.list_price = product.product_id.list_price * (1 - product.discount / 100)
            else:
                product.list_price = product.product_id.list_price * (1 - product.bundle_id.discount_value / 100)



class ProductBundleVariant(models.Model):
    _name = 'product.bundle.variant'
    _inherits = {'product.product': 'product_id'}
    product_id = fields.Many2one(
        'product.product',
        ondelete='cascade')
    product = fields.Many2one('product.bundle.product')
    name = fields.Text('Name')
    bundle_id = fields.Many2one('product.bundle', string="Bundle")
