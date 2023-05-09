from odoo import api, fields, models


class Facebook(models.Model):
    _name = 'facebook'
    access_token = fields.Char()
    token_type = fields.Char()
    expires_in = fields.Char()
    feed_id = fields.Many2one('instafeed')
    page_id = fields.Char()
    instagram_business_account_id = fields.Char()
    fb_username = fields.Char()
    followers_count = fields.Integer(default=0)
    posts = fields.One2many('instagram.post', 'facebook_id')
