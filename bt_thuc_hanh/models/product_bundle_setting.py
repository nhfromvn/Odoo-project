from odoo import models, fields, api
class ProductBundleSettings(models.TransientModel):

    _inherit = 'res.config.settings'
    bundle_position = fields.Selection([('below',"Below add to cart form"),
                                        ('above',"Above add to cart form")],default = 'below')
    bundle_number = fields.Integer()
    bundle_title_color = fields.Char()
    button_label = fields.Char()


