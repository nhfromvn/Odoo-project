from odoo import models, fields, api


class WidgetConfig(models.Model):
    _name = 'widget.config'
    admin = fields.Many2one('res.users')
    widget = fields.Many2one('widget.data')
    feed_title = fields.Char(default='Hello World')
    post_spacing = fields.Integer(default='20')
    on_post_click = fields.Char(default='Open popup/show product')
    layout = fields.Char(default='Grid-Tiles')
    configuration = fields.Char(default='Auto')
    per_slide = fields.Integer(default=3)
    number_of_posts = fields.Integer(default=7)
    number_of_rows = fields.Integer(default=3)
    number_of_columns = fields.Integer(default=3)
    show_likes = fields.Boolean(default=1)
    show_followers = fields.Boolean(default=1)
    display_tag_post = fields.Char()
