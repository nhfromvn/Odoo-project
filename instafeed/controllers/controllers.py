# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import requests
import shutil
import wget
import shopify, json
import base64


class Instafeed(http.Controller):
    @http.route('/instafeed', auth='user')
    def index(self, **kw):
        return request.render('instafeed.instafeed')

    @http.route('/instafeed/error', auth='user')
    def connect_error(self, **kw):
        video = open('video.mp4')
        return ''' <b>This store already connect with other account
                Login to another account or change your connecting store to continue</b> '''

    @http.route('/instafeed/test', auth='user')
    def test(self, **kw):
        # video = requests.get(
        #     'https://v58.tiktokcdn.com/video/tos/alisg/tos-alisg-pve-0037/ooIQADjfWVkgRAobu5g2jfJmMkjnJF8eA1eGjG/?a=1340&ch=0&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&br=848&bt=424&cs=0&ds=3&ft=kLeRqya9Zeb0PD1NCXeXg9wwk.YQkEeC~&mime_type=video_mp4&qs=0&rc=OWVlaGlnOWZkaTVpPDNnPEBpMzw3bjs6ZmlpazMzODgzNEA1YV8xNS1eNjQxXl5iYjA2YSMxMG1ycjRnaW9gLS1kLy1zcw%3D%3D&l=20230611175629A72796AF6DB62234C7C9&VExpiration=1686527808&VSignature=1LgwXFNFKCc1sgmnN7Ju8A&btag=e00080000&cc=14')
        # # print(video.content)
        # base64_video = base64.b64encode(video.content)
        # print(base64_video.decode('utf-8'))
        current_user = request.env.user
        shop = request.env['shopify.store'].sudo().search([('admin', '=', current_user.id)])
        new_session = shopify.Session(shop.url, request.env['ir.config_parameter'].sudo().get_param(
            'instafeed.api_version_instafeed'),
                                      token=shop.access_token)

        shopify.ShopifyResource.activate_session(new_session)
        theme_id = shopify.Theme.find()[0].id
        # asset = shopify.Asset.create({
        #     "theme_id": theme_id,
        #     "key": "assets/asset.mp4",
        #     "src": "https://v39-us.tiktokcdn.com/bc3e96393952e4d935ad2c87a6ff6817/648709a2/video/tos/alisg/tos-alisg-pve-0037/oISOzNM8BhQqEZCohQywfAr3IAK4AiHJNAABJr/?a=1340&ch=0&cr=3&dr=0&lr=all&cd=0%7C0%7C0%7C3&br=1338&bt=669&cs=0&ds=3&ft=74-OgDyjNeLVQx6iUgVjWd.9UKH38lczr7fhyWHrK&mime_type=video_mp4&qs=0&rc=MzZoZDc6NTw1Z2Y3Zjo6M0Bpajs3dGY6ZnhqazMzODgzNEBjXmAzLTUuNTYxM14tX141YSMxY21kcjQwZm9gLS1kLzFzcw%3D%3D&l=2023061206032640196E35568CC3778499&btag=e00080000",
        # })
        asset = shopify.Asset.find('assets/asset.mp4', theme_id=theme_id)
        print(asset)
        return ''' <b>test
                    <br>
                    api</b> '''
