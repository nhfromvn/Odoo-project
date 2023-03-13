from odoo import fields, models, api
import datetime


class SHistoryFetch(models.Model):
    _name = 's.history.fetch'
    published_at_min = fields.Char()
    published_at_max = fields.Char()
    fetch_time = fields.Datetime()
    quantity = fields.Integer()
    store_id = fields.Many2one('s.store.info')
    type = fields.Char()
