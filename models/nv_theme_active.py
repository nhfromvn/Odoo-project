from odoo import models, fields, api


class Theme(models.Model):
    _name = 'nv.theme.active'
    theme_id = fields.Char()
    shop = fields.Many2one('nv.store')
    theme_name = fields.Char()
    is_active = fields.Boolean()
    role = fields.Char('')
