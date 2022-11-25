from odoo import models, fields, api


class ProductBundle(models.Model):
    _name = 'product.bundle'
    user_id = fields.Many2one('res.users', string="Customer")
    name = fields.Char('Name')
    description = fields.Char()
    type = fields.Selection([('bundle', 'Multiple Product Bundle'),
                             ('tier', 'Quantity Break Bundle')],
                            'Type', default='bundle')
    products = fields.One2many('product.bundle.product','bundle_id', String="Products")
    variant_ids = fields.One2many('product.bundle.variant', 'bundle_id', String="Variants")
    discount_rule = fields.Selection([('bundle', 'Discount on total bundle'),
                                      ('product', 'Discount on each product'),
                                      ], default="bundle")
    discount_type = fields.Selection([('percentage', 'Percentage'),
                                      ('hard_fix', 'Hard Fix'),
                                      ('total_fix', 'Total Fix')], default="percentage")

    discount_value = fields.Integer()
    enable = fields.Boolean()
    active = fields.Boolean('Active',default =True)
    priority = fields.Integer()
    start_time = fields.Datetime()
    end_time = fields.Datetime()
    indefinite_bundle = fields.Boolean(default=False)
    tier_quantity = fields.One2many('product.bundle.qty','bundle_id')

    @api.onchange('indefinite_bundle')
    def _change_indefinite(self):
            if self.indefinite_bundle:
                if self.start_time and self.end_time:
                    self.start_time = False
                    self.end_time = False
            else:
                print("do something")

    _sql_constraints = [
        ('name_uniq', 'UNIQUE (name)',
         'Book title must be unique.'),
        ('positive_discount', 'CHECK(discount_value>0)',
         'discount must be positive')
    ]


class User(models.Model):
    _inherit = 'res.users'
    bundle_ids = fields.One2many('product.bundle', 'user_id', string="Bundle")
