from odoo import api, fields, models


class HotspotPrivate(models.Model):
    _name = 'hotspot.private'
    name = fields.Char()
    admin = fields.Many2one('res.users')
    post_id = fields.Many2one('post.private.advance')
    product_id = fields.Char()
# shopify_product_handle = fields.Char()
# shopify_product_img_src = fields.Char()
# shopify_product_variant_num = fields.Integer()
# shopify_product_product_url = fields.Char()
# status = fields.Boolean()
