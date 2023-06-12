from odoo import models, fields, api


class MediaSource(models.Model):
    _name = 'media.source'
    name = fields.Char()
    admin = fields.Many2one('res.users')
    facebook_account = fields.Many2one('facebook.account')
    instagram_account = fields.Many2one('instagram.account')
    social_account = fields.Many2one('social.account')
    selected_private_posts = fields.Many2many('post.private')