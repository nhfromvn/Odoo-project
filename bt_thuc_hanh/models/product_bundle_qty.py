from odoo import models,fields,api
class ProductBundleQuantity(models.Model):
    _name = 'product.bundle.qty'
    is_add_range = fields.Boolean(default = True, onchange = 'change_add_range')
    qty_start = fields.Integer()
    qty_end = fields.Integer()
    to = fields.Text(default ="to")
    discount_value = fields.Integer()
    bundle_id = fields.Many2one('product.bundle', ondelete='set null')
    @api.constrains('qty_start','qty_end')
    def check_qty_range(self):
        if self.qty_start > 0:
            if self.qty_start and self.qty_end:
                raise models.ValidationError(
                        'Quantity must be positive in every cases')
        if self.qty_end >= self.qty_start:
                        raise models.ValidationError(
                            'Quantity must be positive in every cases')
        else:
            print("do some thing")
    @api.onchange('is_add_range')
    def change_add_range(self):
        if not self.is_add_range:
            self.to = " "
            self.qty_end = False
        else:
            self.to = "to"











