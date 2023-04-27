from odoo import api, fields, models


class InstagramUser(models.Model):
    _name = 'instagram.user'
    user_id = fields.Char()
    username = fields.Char()
    posts = fields.One2many('instagram.post', 'user_id')
class InstagramPost(models.Model):

    _name = 'instagram.post'
    media_id = fields.Char()
    user_id = fields.Many2one('instagram.user')
    caption = fields.Char()
    media_type = fields.Char()
    media_url = fields.Char()
    timestamp = fields.Char()
