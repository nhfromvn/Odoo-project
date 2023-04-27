from odoo import http
from odoo.http import request
import json
from odoo import http, fields
from odoo.http import request
import hmac
import hashlib
import requests
import werkzeug
import os
import jinja2
from pytz import timezone
from datetime import datetime
import shopify, binascii, json, string, random

SCOPE = 'user_profile,user_media'


class MetaController(http.Controller):
    @http.route('/instafeed/connect', auth='user')
    def connect_instagram(self, **kwargs):
        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        client_id = request.env['ir.config_parameter'].sudo().get_param('instafeed.ig_app_id')
        return werkzeug.utils.redirect(
            'https://api.instagram.com/oauth/authorize?client_id=' + client_id + '&redirect_uri=' + base_url + '/instafeed/auth&scope=' + SCOPE + '&response_type=code')

    @http.route('/instafeed/auth', type="http", auth="public", website=True, method=['GET'], csrf=False)
    def auth_instagram(self, **kwargs):
        shop_url = request.session['shop_url']
        shop = request.env['shop'].sudo().search([('shop_url', '=', shop_url)])
        enpoint = 'https://api.instagram.com/oauth/access_token'
        client_id = request.env['ir.config_parameter'].sudo().get_param('instafeed.ig_app_id')
        client_secret = request.env['ir.config_parameter'].sudo().get_param('instafeed.secret_key_instagram')
        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        auth_data = {
            'client_id': client_id,
            'code': kwargs['code'],
            'client_secret': client_secret,
            'grant_type': 'authorization_code',
            'redirect_uri': base_url + '/instafeed/auth'
        }
        print(kwargs)
        res = requests.post(enpoint, data=auth_data).json()
        print(res)
        instafeed_user = request.env['instafeed.user'].sudo().search([('store_id', '=', shop.id)], limit=1)
        instafeed_user.write(res)
        return werkzeug.utils.redirect('/instafeed')

    @http.route('/instafeed/get/insta_user', auth='user', csrf=False)
    def get_uer_info(self, **kwargs):
        shop_url = request.session['shop_url']
        shop = request.env['shop'].sudo().search([('shop_url', '=', shop_url)], limit=1)
        instafeed_user = request.env['instafeed.user'].sudo().search([('store_id', '=', shop.id)], limit=1)
        enpoint = 'https://graph.instagram.com/' + instafeed_user.user_id + '?fields=id,username&access_token=' + instafeed_user.access_token
        res = requests.get(enpoint)
        if res.ok:
            print(json.dumps(res.json()))
            instagram_user = request.env['instagram.user'].sudo().search([('user_id', '=', res.json()['id'])], limit=1)
            if instagram_user:
                instagram_user.write({'username': res.json()['username']})
            else:
                instagram_user = request.env['instagram.user'].sudo().create({'user_id': res.json()['id'],
                                                                              'username': res.json()['username']})
            instafeed_user.write({'instagram_user': instagram_user.id})
            return json.dumps(res.json())
        else:
            return False

    @http.route('/instafeed/get/insta_media', auth='user', csrf=False)
    def get_media(self, **kwargs):
        shop_url = request.session['shop_url']
        shop = request.env['shop'].sudo().search([('shop_url', '=', shop_url)])
        instafeed_user = request.env['instafeed.user'].sudo().search([('store_id', '=', shop.id)], limit=1)
        enpoint = 'https://graph.instagram.com/me/media?fields=id,caption&access_token=' + instafeed_user.access_token
        res = requests.get(enpoint)
        if res.ok:
            print(json.dumps(res.json()))
            for post in res.json()['data']:
                post_exist = request.env['instagram.post'].sudo().search(
                    ['&', ('media_id', '=', post['id']), ('user_id', '=', instafeed_user.instagram_user.user_id)],
                    limit=1)
                # if post_exist:
                #     if not post['caption'] == None:
                #         post_exist.write({'caption': post['caption']})
                # else:
                post_exist = request.env['instagram.post'].sudo().create({'media_id': post['id'],
                                                                          'user_id': instafeed_user.instagram_user.id})
            resp = requests.get(
                'https://graph.instagram.com/18258967933146884?fields=id,media_type,media_url,username,timestamp&access_token=' + instafeed_user.access_token
            )
            print(json.dumps(resp.json()))
            return json.dumps(res.json())
        else:
            return False
    @http.route('/facebook/auth', type="http", auth="public", website=True, method=['GET'], csrf=False)
    def facebook_auth(self, **kwargs):
        print(kwargs)
