# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Instafeed(models.Model):
    _name = 'instafeed'
    store_id = fields.Many2one('shop')
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
    user_id = fields.Char(default='')
    access_token = fields.Char()
    long_live_access_token = fields.Char()
    username = fields.Char(default='')


class InstafeedConfig(models.TransientModel):
    _inherit = 'res.config.settings'
    api_key_instafeed = fields.Char()
    secret_key_instafeed = fields.Char()
    ig_app_id = fields.Char()
    # api_key_instagram = fields.Char()
    secret_key_instagram = fields.Char()
    fb_app_id = fields.Char()
    # api_key_facebook = fields.Char()
    secret_key_facebook = fields.Char()

    @api.model
    def get_values(self):
        res = super().get_values()
        params = self.env['ir.config_parameter'].sudo()
        res.update(
            api_key_instafeed=str(params.get_param('instafeed.api_key_instafeed')),
            secret_key_instafeed=str(params.get_param('instafeed.secret_key_instafeed')),
            ig_app_id=str(params.get_param('instafeed.ig_app_id')),
            # api_key_instagram=str(params.get_param('instafeed.api_key_instagram')),
            secret_key_instagram=str(params.get_param('instafeed.secret_key_instagram')),
            fb_app_id=str(params.get_param('instafeed.fb_app_id')),
            # api_key_facebook=str(params.get_param('instafeed.api_key_facebook')),
            secret_key_facebook=str(params.get_param('instafeed.secret_key_facebook')),
        )
        return res

    def set_values(self):
        super().set_values()
        param = self.env['ir.config_parameter'].sudo()
        field_api_key = self.api_key_instafeed if self.api_key_instafeed else False
        field_secret_key = self.secret_key_instafeed if self.secret_key_instafeed else False
        field_ig_app_id = self.ig_app_id if self.ig_app_id else False
        # field_api_key_instagram = self.api_key_instagram if self.api_key_instagram else False
        field_secret_key_instagram = self.secret_key_instagram if self.secret_key_instagram else False
        field_fb_app_id = self.fb_app_id if self.fb_app_id else False
        # field_api_key_facebook = self.api_key_facebook if self.api_key_facebook else False
        field_secret_key_facebook = self.secret_key_facebook if self.secret_key_facebook else False

        param.set_param('instafeed.api_key_instafeed', field_api_key)
        param.set_param('instafeed.secret_key_instafeed', field_secret_key)
        param.set_param('instafeed.ig_app_id', field_ig_app_id)
        # param.set_param('instafeed.api_key_instagram', field_api_key_instagram)
        param.set_param('instafeed.secret_key_instagram', field_secret_key_instagram)
        param.set_param('instafeed.fb_app_id', field_fb_app_id)
        # param.set_param('instafeed.api_key_facebook', field_api_key_facebook)
        param.set_param('instafeed.secret_key_facebook', field_secret_key_facebook)
