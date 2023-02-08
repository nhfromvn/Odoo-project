from odoo import models, fields, api


class ShopifyProduct(models.Model):
    _name = 'sp.product'
    _description = 'Products'
    _rec_name = 'name'
    product_id = fields.Char()
    store_id = fields.Many2one("sp.shop")
    name = fields.Char()
    price = fields.Float()
