from odoo import models, fields, api


class order(models.Model):
    _inherit = "sale.order"
    customer_discount_code = fields.Text(string="Discount code", group = "1. Advanced Sale")
    discount = fields.Integer()
    check_discount = fields.Boolean(
        string='Check Discount',
        compute='_compute_check_discount',
        store=True
    )

    @api.depends('customer_discount_code')
    def _compute_check_discount(self):
        for order1 in self:
            if order1.discount:
                if order1.customer_discount_code == "VIP" + "_" + str(order1.discount):
                    order1.check_discount = True
                else:
                    order1.check_discount = False
            else:
                order1.check_discount = False

    @api.constrains('customer_discount_code')
    def _check_discount_validation(self):
        for product in self:
            if product.customer_discount_code != "VIP" + "_" + str(product.discount):
                raise models.ValidationError(
                    'Invalid form')
    def update_discount_code(self):
        for order in self:
            print(order.customer_discount_code)

class plan_sale_oder(models.Model):
    _inherit = "sale.order.line"
    customer_discount_code = fields.Text(string="Discount code")
    sale_order_discount_estimated = fields.Float(
        string='Estimated order discount',
        compute='_compute_discount',
    )

    @api.constrains('customer_discount_code')
    def _check_discount_validation(self):
        for product in self:
            if product.customer_discount_code != "VIP" + "_" + str(product.discount):
                raise models.ValidationError(
                    'Invalid form')

    @api.depends('discount')
    def _compute_discount(self):
        for product in self:
            estimate = product.price_reduce_taxinc * (1 - product.discount / 100)


class customer(models.Model):
    _inherit = "res.partner"
    customer_discount_code = fields.Text(string="Discount code")
