from odoo import models, fields, api


class ProductBundleProduct(models.Model):
    _name = 'product.bundle.product'
    _inherits = {'product.product': 'product_id'}

    product_id = fields.Many2one(
        'product.product',
        ondelete='cascade')
    bundle_id = fields.Many2one('product.bundle', string="Bundle")
    name = fields.Char('Name')
    quantity = fields.Float('Quantity')
    product_vendor = fields.Many2one('res.partner', string="Product Vendor")
    discount = fields.Float()
    list_price = fields.Float(compute='_compute_price')
    list_price_bundle = fields.Float()
    image = fields.Binary(attachment=True)
    bundle_date = fields.Date.today()
    @api.depends('product_id.list_price')
    def _compute_price(self):
        for product in self:
            if product.bundle_id.discount_rule == 'product':
                if product.bundle_id.discount_type == 'total_fix':
                    product.list_price = product.product_id.list_price - product.discount
                elif product.bundle_id.discount_type == 'hard_fix':
                    product.list_price = product.discount
                else:
                    product.list_price = product.product_id.list_price * (1 - product.discount / 100)


