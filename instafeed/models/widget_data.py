from odoo import models, fields, api


class WidgetData(models.Model):
    _name = 'widget.data'
    media_sources = fields.Many2many('media.source')
    name = fields.Char()
    admin = fields.Many2one('res.users')
    hashed_id = fields.Char()
    widget_config = fields.Many2one('widget.config')
