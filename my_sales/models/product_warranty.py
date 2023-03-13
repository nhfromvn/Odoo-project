from odoo import models, fields, api

def to_valid_from(day):
    return  str(day) if  day > 10 else '0'+str(day)
def to_valid_year_from(year):
    return  str(year) if  year < 99 else str(year%100)

class product(models.Model):
    _inherit = 'product.template'
    product_warranty_code = fields.Text(string="Warranty Code",
                                        compute="_compute_warranty"
                                       )
    Date_from = fields.Date(string="Date From")
    Date_to = fields.Date(string="Date To")
    discount = fields.Float(compute = "_receive_discount",string='Discount (%)', digits='Discount', default=0.0)
    Sale_order_discount_estimated = fields.Monetary(
                                    compute ="_compute_discount",
                                    )
    Calculated_discount_total = fields.Integer(compute = "_count_discount",
                                               store= True,
                                               )
    interval_warranty_days =fields.Integer(compute="_compute_check_warranty")
    @api.constrains('product_warranty_code')
    def _check_product_validation(self):
        for product in self:
            if product.Date_from and product.Date_to:
                if product.product_warranty_code != "PWR" + "/" + to_valid_from(product.Date_from.day)+to_valid_from(product.Date_from.month)+to_valid_year_from(product.Date_from.year) + "/" + to_valid_from(product.Date_to.day)+to_valid_from(product.Date_to.month) + to_valid_year_from(product.Date_to.year):
                    raise models.ValidationError('Invalid form')
    @api.depends('Date_from', 'Date_to')
    def _compute_warranty(self):
        for product in self:
            if product.Date_from and product.Date_to:
                product.product_warranty_code = "PWR" + "/" + to_valid_from(product.Date_from.day)+to_valid_from(product.Date_from.month)+to_valid_year_from(product.Date_from.year) + "/" + to_valid_from(product.Date_to.day)+to_valid_from(product.Date_to.month) + to_valid_year_from(product.Date_to.year)

            else:
                product.product_warranty_code = False
    @api.depends('discount')
    def _receive_discount(self):
        for product in self:
            if product.product_warranty_code :
                product.discount = 0
            else:
                product.discount = 10

    @api.depends('discount', 'list_price')
    def _compute_discount(self):
        for product in self:
            if product.discount:
                product.Sale_order_discount_estimated = product.list_price*float(product.discount)/100
            else:
                product.Sale_order_discount_estimated = product.list_price

    @api.depends('discount')
    def _count_discount(self):
        for product in self:
            if product.discount:
                product.Calculated_discount_total+=1
    @api.depends('Date_to')
    def _compute_check_warranty(self):
        today = fields.Date.today()
        for product in self:
            if product.product_warranty_code:
                if today < product.Date_to:
                  delta =product.Date_to-today
                  product.interval_warranty_days = delta.days

                else:
                    product.interval_warranty_days = False
            else:
                product.interval_warranty_days = False




