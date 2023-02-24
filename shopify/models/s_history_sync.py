from odoo import fields, models, api
import datetime


class SHistorySync(models.Model):
    _name = 's.history.sync'
    time = fields.Datetime()
    date_from = fields.Char()
    date_to = fields.Char()
    store_id = fields.Many2one('s.store.info')
    payment = fields.Integer()
    invoice = fields.Integer()
