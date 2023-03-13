# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class customaddons/bought_together(models.Model):
#     _name = 'customaddons/bought_together.customaddons/bought_together'
#     _description = 'customaddons/bought_together.customaddons/bought_together'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
