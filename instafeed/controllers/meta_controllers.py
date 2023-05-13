from odoo import http
from odoo.http import request
import requests
import werkzeug

IG_SCOPE = 'user_profile,user_media'
FB_SCOPE = 'pages_show_list, instagram_basic, pages_manage_engagement'


class MetaController(http.Controller):
    @http.route('/instafeed/connect', auth='user')
    def connect_instagram(self, **kwargs):
        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        client_id = request.env['ir.config_parameter'].sudo().get_param('instafeed.ig_app_id')
        return werkzeug.utils.redirect(
            'https://api.instagram.com/oauth/authorize?client_id=' + client_id + '&redirect_uri=' + base_url + '/instafeed/auth&scope=' + IG_SCOPE + '&response_type=code')

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
        instafeed_users = request.env['instafeed'].sudo().search([('store_id', '=', shop.id)])
        for instafeed_user in instafeed_users:
            instafeed_user.write(res)
        return werkzeug.utils.redirect('/instafeed')

    @http.route('/instafeed/facebook/connect', auth='user')
    def fb_connect(self, **kwargs):
        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        client_id = request.env['ir.config_parameter'].sudo().get_param('instafeed.fb_app_id')

        return werkzeug.utils.redirect(
            'https://www.facebook.com/v12.0/dialog/oauth?client_id=' + client_id + '&redirect_uri=' + base_url + '/instafeed/facebook/auth&scope=' + FB_SCOPE + '&response_type=code')

    @http.route('/instafeed/facebook/auth', auth='public', type='http')
    def fb_auth(self, **kwargs):
        shop_url = request.session['shop_url']
        shop = request.env['shop'].sudo().search([('shop_url', '=', shop_url)])
        enpoint = 'https://graph.facebook.com/v12.0/oauth/access_token'
        client_id = request.env['ir.config_parameter'].sudo().get_param('instafeed.fb_app_id')
        client_secret = request.env['ir.config_parameter'].sudo().get_param('instafeed.secret_key_facebook')
        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        auth_data = {
            'client_id': client_id,
            'code': kwargs['code'],
            'client_secret': client_secret,
            'grant_type': 'authorization_code',
            'redirect_uri': base_url + '/instafeed/facebook/auth'
        }
        print(kwargs)
        res = requests.post(enpoint, data=auth_data).json()
        instafeed_users = request.env['instafeed'].sudo().search([('store_id', '=', shop.id)])
        for instafeed_user in instafeed_users:
            facebook_user = request.env['facebook'].sudo().search([('feed_id', '=', instafeed_user.id)], limit=1)
            if facebook_user:
                facebook_user.write(res)
            else:
                res['feed_id'] = instafeed_user.id
                request.env['facebook'].sudo().create(res)
        print(res)

        return werkzeug.utils.redirect('/instafeed')

    @http.route('/instafeed/facebook/logout', auth='public', type='http')
    def fb_logout(self):
        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        shop_url = request.session['shop_url']
        shop = request.env['shop'].sudo().search([('shop_url', '=', shop_url)])
        instafeed_user = request.env['instafeed'].sudo().search([('store_id', '=', shop.id)], limit=1)
        facebook_user = request.env['facebook'].sudo().search([('feed_id', '=', instafeed_user.id)])
        return werkzeug.utils.redirect(
            'https://www.facebook.com/logout.php?next=' + base_url + '/instafeed' + '&access_token=' + facebook_user.access_token)
