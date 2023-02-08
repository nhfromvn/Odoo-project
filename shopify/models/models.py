# -*- coding: utf-8 -*-
import datetime

import shopify

from odoo import models, fields, api

class SApp(models.Model):
    _name = 's.app'
    _description = 'Shopify App'

    name = fields.Char(index=True)
    sp_api_key = fields.Char()
    sp_api_secret_key = fields.Char()
    sp_api_version = fields.Char()
    gg_api_client_id = fields.Char()
    gg_api_client_secret = fields.Char()
    cdn_tag = fields.Char()
    # them cac truong can thiet

    def update_cdn_tag(self):
        timestamp = str(datetime.datetime.utcnow().timestamp())
        self.cdn_tag = '#base' + '#path_to_script?v' + str(timestamp)

class SSpShop(models.Model):
    _name = 's.sp.shop'
    _rec_name = 'name'

    name = fields.Char()
    base_url = fields.Char(index=True)
    base_url_2 = fields.Char(string="Base url 2", index=True)
    password = fields.Char(groups="base.group_system")
    email = fields.Char()
    status = fields.Boolean()
    currency_code = fields.Char()
    # them cac truong can thiet

class SSpApp(models.Model):
    _name = 's.sp.app'
    _rec_name = 'sp_shop_id'

    sp_shop_id = fields.Many2one('s.sp.shop')
    s_app_id = fields.Many2one('s.app')
    status = fields.Boolean()
    token = fields.Char()
    webhook_data = fields.Char()
    # them cac truong can thiet

    def add_webhook_to_shop(self, topic_name, path):
        self.ensure_one()
        full_path = '#base_url' + path
        # use ngrok https test tren local
        # full_path = 'https://e86fea37e12f.ngrok.io' + path
        webhook = shopify.Webhook()
        webhook.topic = topic_name
        webhook.address = full_path
        webhook.format = 'json'
        webhook.save()

    def add_script_tag_to_shop(self):
        src = self.s_app_id.cdn_tag
        # check exist script tag
        shopify.ScriptTag.find()
        # neu chua ton tai tao moi
        scriptTag = shopify.ScriptTag.create({
            "event": "onload",
            "src": src
        })
        return scriptTag.id