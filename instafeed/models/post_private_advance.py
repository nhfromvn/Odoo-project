from odoo import models, fields, api


class PostPrivate(models.Model):
    _name = 'post.private.advance'
    post_id = fields.Char()
    facebook_user = fields.Many2one('facebook.account')
    media_url = fields.Char()
    type = fields.Char()
    caption = fields.Char()
    insta_profile_link = fields.Char()
    thumbnail_url = fields.Char()
    hotspot = fields.One2many('hotspot.private', 'post_id')
    admin = fields.Many2one('res.users')
    like_count = fields.Char()
    comments_count = fields.Char()
    create_date = fields.Date()
    link_to_post = fields.Char()
    list_tags = fields.Char()
