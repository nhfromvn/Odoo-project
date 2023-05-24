from odoo import http
from odoo.http import request
import requests
import werkzeug

IG_SCOPE = 'user_profile,user_media'
FB_SCOPE = 'pages_show_list, instagram_basic, pages_manage_engagement'


class MetaController(http.Controller):
    #     @http.route('/instafeed/connect', auth='user')
    #     def connect_instagram(self, **kwargs):
    #         base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
    #         client_id = request.env['ir.config_parameter'].sudo().get_param('instafeed.ig_app_id')
    #         return werkzeug.utils.redirect(
    #             'https://api.instagram.com/oauth/authorize?client_id=' + client_id + '&redirect_uri=' + base_url + '/instafeed/auth&scope=' + IG_SCOPE + '&response_type=code')
    #
    #     @http.route('/instafeed/auth', type="http", auth="public", website=True, method=['GET'], csrf=False)
    #     def auth_instagram(self, **kwargs):
    #         shop_url = request.session['shop_url']
    #         shop = request.env['shop'].sudo().search([('shop_url', '=', shop_url)])
    #         enpoint = 'https://api.instagram.com/oauth/access_token'
    #         client_id = request.env['ir.config_parameter'].sudo().get_param('instafeed.ig_app_id')
    #         client_secret = request.env['ir.config_parameter'].sudo().get_param('instafeed.secret_key_instagram')
    #         base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
    #         auth_data = {
    #             'client_id': client_id,
    #             'code': kwargs['code'],
    #             'client_secret': client_secret,
    #             'grant_type': 'authorization_code',
    #             'redirect_uri': base_url + '/instafeed/auth'
    #         }
    #         print(kwargs)
    #         res = requests.post(enpoint, data=auth_data).json()
    #         print(res)
    #         instafeed_users = request.env['instafeed'].sudo().search([('store_id', '=', shop.id)])
    #         for instafeed_user in instafeed_users:
    #             instafeed_user.write(res)
    #         new_enpoint = "https://graph.instagram.com/access_token?grant_type=ig_exchange_token&client_secret=" + client_secret + "&access_token=" + \
    #                       instafeed_users[0].access_token
    #         new_res = requests.get(new_enpoint).json()
    #         print(new_res)
    #         for instafeed_user in instafeed_users:
    #             instafeed_user.write({'long_live_access_token': new_res['access_token']})
    #         return werkzeug.utils.redirect('/instafeed')
    #
    @http.route('/instafeed/facebook/connect', auth='user')
    def fb_connect(self, **kwargs):
        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        client_id = request.env['ir.config_parameter'].sudo().get_param('instafeed.fb_app_id')

        return werkzeug.utils.redirect(
            'https://www.facebook.com/v12.0/dialog/oauth?client_id=' + client_id + '&redirect_uri=' + base_url + '/instafeed/facebook/auth&scope=' + FB_SCOPE + '&response_type=code')

    @http.route('/instafeed/facebook/auth', auth='public', type='http')
    def fb_auth(self, **kwargs):
        try:
            current_user = request.env.user
            shop = request.env['shopify.store'].sudo().search([("admin", '=', current_user.id)], limit=1)
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
            new_enpoint = 'https://graph.facebook.com/v12.0/me?fields=picture{url},accounts{instagram_business_account{followers_count,username}},name&access_token=' + \
                          res['access_token']
            new_res = requests.get(new_enpoint).json()
            print(res)
            print(new_res)
            facebook_account = request.env['facebook.account'].sudo().search(
                [('admin', '=', current_user.id), ('user_id', '=', new_res['id'])])
            if facebook_account:
                facebook_account.write({'access_token': res['access_token'],
                                        'username': new_res['name'],
                                        'url_image': new_res['picture']['data']['url'],
                                        'instagram_business_account_id':
                                            new_res['accounts']['data'][0]['instagram_business_account']['id'],
                                        'instagram_business_account_followers_count':
                                            new_res['accounts']['data'][0]['instagram_business_account'][
                                                'followers_count'],
                                        'instagram_business_account_username':
                                            new_res['accounts']['data'][0]['instagram_business_account'][
                                                'username']
                                        },
                                       )
            else:
                facebook_account = request.env['facebook.account'].sudo().create({
                    'admin': current_user.id,
                    'access_token': res['access_token'],
                    'status': True,
                    'user_id': new_res['id'],
                    'username': new_res['name'],
                    'url_image': new_res['picture']['data']['url'],
                    'instagram_business_account_id':
                        new_res['accounts']['data'][0]['instagram_business_account']['id'],
                    'instagram_business_account_followers_count':
                        new_res['accounts']['data'][0]['instagram_business_account']['followers_count'],
                    'instagram_business_account_username':
                        new_res['accounts']['data'][0]['instagram_business_account'][
                            'username']
                })
            facebook_account.get_posts()
            return werkzeug.utils.redirect('/instafeed')
        except Exception as e:
            print(e)
        return werkzeug.utils.redirect('/instafeed')
