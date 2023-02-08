import json

from odoo import models, fields, api


class SAppDiscount(models.Model):
    _name = 'shopify.discount'

    name = fields.Char(index=True)
    discount_type = fields.Selection([('per', '%'), ('amount', 'Amount')])
    discount_amount = fields.Float()
    products = fields.One2many('shopify.discount.products', 'shop_discount_id')


class SAppDiscountProduct(models.Model):
    _name = 'shopify.discount.products'

    shop_discount_id = fields.Many2one('shopify.discount')
    product_id = fields.Char()
    product_name = fields.Char()
    product_handle = fields.Char()
    qty = fields.Integer()


class SAppDiscountSettings(models.Model):
    _name = 'shopify.discount.settings'

    font_color = fields.Char()
    add_to_cart_color = fields.Char()
    position = fields.Char()
    # ...


class SAppDiscountData(models.Model):
    _name = 'shopify.discount.data'

    discount_id = fields.Many2one('shopify.discount')
    add_to_cart_count = fields.Integer()
    sale = fields.Float()


class SAppDiscountDataReport(models.Model):
    _name = 'shopify.discount.report'

    date_start = fields.Date()
    date_end = fields.Date()
    data = fields.Text(compute='get_data')
    discount_id = fields.Many2one('shopify.discount')

    @api.depends('date_start', 'date_end', 'discount_id')
    def get_data(self):
        data = {}
        # xu ly lay du lieu shop
        # update vao data
        self.data = json.dumps(data)
