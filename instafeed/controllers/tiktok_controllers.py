from odoo import http
from odoo.http import request
import requests
import werkzeug
import random

SCOPES = 'user.info.basic,video.list'


class TiktokControllers(http.Controller):
    @http.route('/tiktok/connect', auth='user')
    def connect_tiktok(self, **kwargs):
        csrfstate = str(random.random())[2:]
        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        client_id = request.env['ir.config_parameter'].sudo().get_param('instafeed.tiktok_app_id')
        return werkzeug.utils.redirect(
            'https://tiktok.com/auth/authorize?client_key=' + client_id + '&redirect_uri=' + base_url + '/tiktok/auth&scope=' + SCOPES + '&response_type=code')

    # @http.route('/tiktok', auth='user')
    # def auth_tiktok(self, **kwargs):
    #     print('hahahaha')
    #     print(kwargs)
    #     return "<blockquote class=\"tiktok-embed\" cite=\"https://www.tiktok.com/@scout2015/video/6718335390845095173\" data-video-id=\"6718335390845095173\" data-embed-from=\"oembed\" style=\"max-width: 605px;min-width: 325px;\" > <section> <a target=\"_blank\" title=\"@scout2015\" href=\"https://www.tiktok.com/@scout2015?refer=embed\">@scout2015</a> <p>Scramble up ur name & I’ll try to guess it😍❤️ <a title=\"foryoupage\" target=\"_blank\" href=\"https://www.tiktok.com/tag/foryoupage?refer=embed\">#foryoupage</a> <a title=\"petsoftiktok\" target=\"_blank\" href=\"https://www.tiktok.com/tag/petsoftiktok?refer=embed\">#petsoftiktok</a> <a title=\"aesthetic\" target=\"_blank\" href=\"https://www.tiktok.com/tag/aesthetic?refer=embed\">#aesthetic</a></p> <a target=\"_blank\" title=\"♬ original sound - 𝐇𝐚𝐰𝐚𝐢𝐢𓆉\" href=\"https://www.tiktok.com/music/original-sound-6689804660171082501?refer=embed\">♬ original sound - 𝐇𝐚𝐰𝐚𝐢𝐢𓆉</a> </section> </blockquote> <script async src=\"https://www.tiktok.com/embed.js\"></script>"

    @http.route('/tiktok/auth', auth='user')
    def oauth_tiktok(self, **kwargs):
        try:
            print(kwargs)
            current_user = request.env.user
            shop = request.env['shopify.store'].sudo().search([("admin", '=', current_user.id)], limit=1)
            code = kwargs['code']
            client_id = request.env['ir.config_parameter'].sudo().get_param('instafeed.tiktok_app_id')
            client_secret = request.env['ir.config_parameter'].sudo().get_param('instafeed.secret_key_tiktok')
            base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
            enpoint = f'https://open-api.tiktok.com/oauth/access_token/?client_key={client_id}&client_secret={client_secret}&code={code}&grant_type=authorization_code'
            res = requests.post(enpoint).json()
            tiktok_user = request.env['social.account'].sudo().search(
                [('type', '=', 'tiktok'), ('admin', '=', current_user.id), ('user_id', '=', res['data']['open_id'])])
            if not tiktok_user:
                instagram_user = request.env['social.account'].sudo().create({
                    'admin': current_user.id,
                    'user_id': res['data']['open_id'],
                    'access_token': res['data']['access_token'],
                    'type': 'tiktok'
                })
            else:
                tiktok_user.write({'access_token': res['data']['access_token']})
            tiktok_user.get_data()
            print(res)
            return werkzeug.utils.redirect('/instafeed')
        except Exception as e:
            print(e)
