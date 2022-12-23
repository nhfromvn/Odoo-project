from odoo import models,fields,api
class ProductBundleReport(models.Model):
    _name = 'product.bundle.reports'
    bundle_id =fields.Integer()
    product_id = fields.Integer()
    save_id = fields.Integer()
    sale_id = fields.Integer(default = 0)

