from odoo import fields, api, models


class ShopifyProduct(models.Model):
    _name = 'shopify.product'
    store_id = fields.Many2one('shop')
    name = fields.Char(string='Product Name')
    product_id = fields.Char()
    image_url = fields.Char()
    price = fields.Float()
    compare_at_price = fields.Float()
    qty_in_stock = fields.Integer()
    is_recommend = fields.Boolean()
    _description = 'Products'
    _rec_name = 'name'
    variant_id = fields.Char()
    widget =fields.Many2one('bought.widget')