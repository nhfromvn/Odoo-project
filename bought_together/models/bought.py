from odoo import  fields,api,models
class Bought(models.Model):
    _name = 'bought'
    name = fields.Char()