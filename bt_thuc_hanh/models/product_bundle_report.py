from odoo import models,fields,api
class ProductBundleReport(models.Model):
    _name = 'product.bundle.reports'
    bundle_id =fields.Integer()
    product_id = fields.Integer()
    total_save = fields.Integer()
    total_sale = fields.Float(default = 0)

