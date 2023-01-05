from odoo import models, fields, api


class ProductBundle(models.Model):
    _name = 'product.bundle'
    total_sale = fields.Text()
    name = fields.Char('Name')
    description = fields.Char()
    type = fields.Selection([('bundle', 'Multiple Product Bundle'),
                             ('tier', 'Quantity Break Bundle')],
                            'Type', default='bundle')
    products = fields.One2many('product.bundle.product', 'bundle_id', String="Products")
    product2 = fields.Many2one('product.product', String="Product Tier")
    discount_rule = fields.Selection([('bundle', 'Discount on total bundle'),
                                      ('product', 'Discount on each product'),
                                      ], default="bundle")
    discount_type = fields.Selection([('percentage', 'Percentage'),
                                      ('total_fix', 'Total Fix'),
                                      ('hard_fix', 'Hard Fix')], default="percentage")
    discount_value = fields.Float()
    discount_value_percent = fields.Float()
    active = fields.Boolean('Active', default=True)
    priority = fields.Integer()
    start_time = fields.Datetime()
    end_time = fields.Datetime()
    indefinite_bundle = fields.Boolean(default=False)
    tier_quantity = fields.One2many('product.bundle.qty', 'bundle_id')
    image = fields.Binary(attachment=True)
    total_price = fields.Float(compute='_compute_total')
    subtotal_price = fields.Float(compute='_compute_subtotal')
    is_active = fields.Boolean(compute='_check_time', default=True)
    today = fields.Datetime.today()
    tier_unit_price = fields.Float(compute="_tier_unit_compute")
    enable = fields.Boolean(default=False)
    @api.depends('type', 'tier_quantity.discount_value')
    def _tier_unit_compute(self):
        for bundle in self:
            if bundle.discount_type == "percentage":
                bundle.tier_unit_price = bundle.product2.list_price * (1 - bundle.tier_quantity.discount.value)
            elif bundle.discount_type == "total_fix":
                bundle.tier_unit_price = bundle.product2.list_price - bundle.tier_quantity.discount_value
            else:
                bundle.tier_unit_price = bundle.tier_quantity.discount_value

    @api.depends('products.list_price')
    def _compute_total(self):
        for bundle in self:
            if bundle.type == 'bundle':
                if bundle.discount_rule == 'product':
                    bundle.total_price = 0
                    for product in bundle.products:
                        bundle.total_price += product.list_price * product.quantity
                if bundle.discount_rule == 'bundle':
                    if bundle.discount_type == 'total_fix':
                        bundle.total_price = bundle.subtotal_price - bundle.discount_value
                    elif bundle.discount_type == 'hard_fix':
                        bundle.total_price = bundle.discount_value
                    else:
                        bundle.total_price += bundle.subtotal_price * (1 - bundle.discount_value / 100)

    @api.depends('products.product_id.list_price')
    def _compute_subtotal(self):
        for bundle in self:
            bundle.subtotal_price = 0
            if bundle.type == 'bundle':
                for product in bundle.products:
                    bundle.subtotal_price += product.product_id.list_price * product.quantity

    @api.onchange('indefinite_bundle')
    def _change_indefinite(self):
        if self.indefinite_bundle:
            self.is_active = True

    @api.constrains('discount_value', 'discount_rule')
    def _check_discount_rule(self):
        for bundle in self:
            if bundle.discount_rule == 'bundle' and bundle.type != 'tier':
                if bundle.discount_value <= 0:
                    raise models.ValidationError(
                        'Discount value must be positive')

    @api.depends('start_time', 'end_time', 'indefinite_bundle')
    def _check_time(self):
        if self.indefinite_bundle:
            self.is_active = True
        else:
            if self.start_time and self.end_time:
                if (self.start_time > self.today) or (self.end_time < self.today):
                    self.is_active = False
                else:
                    self.is_active = True
            else:
                if (self.start_time > self.today) or (self.end_time < self.today):
                    self.is_active = False
                else:
                    self.is_active = True


class SaleOderLineInherit(models.Model):
    _inherit = 'sale.order.line'
    qty_not_in_bundle = fields.Float()
    qty_in_bundle = fields.Float()
class SaleOderLineInherit(models.Model):
    _inherit = 'sale.order'
    amount_bundle = fields.Float()

