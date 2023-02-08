from odoo import api,models,fields
class ShopifyShop(models.Model):
    _name = 'sp.shop'
    name = fields.Char()
    shop_url = fields.Char(index=True)
    base_url_2 = fields.Char(string="Base url 2", index=True)
    password = fields.Char(groups="base.group_system")
    email = fields.Char()
    status = fields.Boolean()
    token = fields.Char()
    currency_code = fields.Char()
    country = fields.Char()

