from odoo import http
from odoo.http import request
import requests
import werkzeug

SCOPE = 'user.info.basic'


class TiktokControllers(http.Controller):
    @http.route('/tiktok/connect', auth='user')
    def connect_tiktok(self, **kwargs):
        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        client_id = request.env['ir.config_parameter'].sudo().get_param('instafeed.tiktok_app_id')
        url =f"https://www.tiktok.com/v2/auth/authorize/?client_key={client_id}&scope=user.info.basic&response_type=code&redirect_uri={base_url}/tiktok"
        return werkzeug.utils.redirect(url)

    @http.route('/tiktok', auth='user')
    def auth_tiktok(self, **kwargs):
        print('hahahaha')
        print(kwargs)
