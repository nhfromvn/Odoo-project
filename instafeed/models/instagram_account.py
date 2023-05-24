from odoo import fields, api, models


class InstagramAccount(models.Model):
    _name = 'instagram.account'
    user_name = fields.Char()
    admin = fields.Many2one('res.users')
    url_image = fields.Char()
    access_token = fields.Char()
    user_id = fields.Char()
    status = fields.Boolean()
