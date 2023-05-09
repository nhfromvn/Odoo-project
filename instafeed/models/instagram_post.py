from odoo import api, fields, models


class InstagramPost(models.Model):
    _name = 'instagram.post'
    post_id = fields.Char()
    products = fields.Many2many('shopify.product', 'post_id')
    facebook_id = fields.Many2one('facebook')


class ShopifyProduct(models.Model):
    _inherit = 'shopify.product'
    post_id = fields.Many2many('instagram.post', 'products')
