from odoo import models, fields, api


class PostPrivate(models.Model):
    _name = 'post.private'
    post_id = fields.Char()
    instagram_user = fields.Many2one('instagram.account')
    media_url = fields.Char()
    type = fields.Char()
    caption = fields.Char()
    insta_profile_link = fields.Char()
    thumbnail_url = fields.Char()
    hotspot = fields.One2many('hotspot.private', 'post_id')
    admin = fields.Many2one('res.users')
    create_date = fields.Date()
