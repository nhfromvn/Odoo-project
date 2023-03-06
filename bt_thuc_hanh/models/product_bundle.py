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
    is_active = fields.Boolean(compute='_check_time_2', default=True)
    today = fields.Datetime.today()
    enable = fields.Boolean(default=False)

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

    @api.constrains('start_time', 'end_time')
    def _check_time(self):
        if self.start_time>= self.end_time:
            raise models.ValidationError(
                'End time must come after start time')


    @api.depends('start_time', 'end_time', 'indefinite_bundle')
    def _check_time_2(self):
        if self.indefinite_bundle:
            self.is_active = True
        else:
            if self.start_time and self.end_time:
                if (self.start_time > self.today) or (self.end_time < self.today):
                    self.is_active = False
                else:
                    self.is_active = True
            else:
                # if (self.start_time > self.today) or (self.end_time < self.today):
                #     self.is_active = False
                # else:
                self.is_active = True


class SaleOderLineInherit(models.Model):
    _inherit = 'sale.order.line'
    qty_not_in_bundle = fields.Float()
    qty_in_bundle = fields.Float()


class SaleOderInherit(models.Model):
    _inherit = 'sale.order'
    amount_bundle = fields.Float()
    discount_on_cart = fields.Float(compute='_compute_discount_on_cart')
    is_active_bundle = fields.Boolean(default=False, compute='_compute_is_active_bundle')

    @api.depends('amount_untaxed', 'amount_total')
    def _compute_discount_on_cart(self):
        self.discount_on_cart = self.amount_untaxed - self.amount_total

    @api.depends('amount_untaxed', 'amount_total')
    def _compute_is_active_bundle(self):
        if self.amount_untaxed == self.amount_total:
            self.is_active_bundle = False
        else:
            self.is_active_bundle = True
