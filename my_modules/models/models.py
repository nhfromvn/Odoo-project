# -*- coding: utf-8 -*-

from odoo import models, fields, api


class customers(models.Model):
    _inherit = 'res.partner'
    customer_rank = fields.Text()
    supplier_rank = fields.Text()