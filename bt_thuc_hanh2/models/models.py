# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class bt_thuc_hanh2(models.Model):
#     _name = 'bt_thuc_hanh2.bt_thuc_hanh2'
#     _description = 'bt_thuc_hanh2.bt_thuc_hanh2'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
