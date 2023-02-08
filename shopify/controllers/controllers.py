import json
import random
import string

import shopify
import werkzeug

from odoo import http
from odoo.http import request

# 1. thực hiện quá trình Oauth 2 để lấy token và lưu vào database

class SpController(http.Controller):

    # generate permission URL
    @http.route('/shopify/auth/app', auth='public')
    def shopify_auth_name(self, name, **kw):
        if 'shop' in kw:
            # generate permission url
            # find app
            current_app = request.env.ref('#app_external_id').sudo()
            if current_app:
                shopify.ShopifyResource.clear_session()
                shopify.Session.setup(
                    api_key=current_app.sp_api_key,
                    secret=current_app.sp_api_secret_key)
                shopify_session = shopify.Session(kw['shop'], current_app.sp_api_version)
                scope = [
                    "read_products",
                    "read_script_tags",
                ]
                redirect_uri = current_app.base_url + "/shopify/finalize/app"
                permission_url = shopify_session.create_permission_url(
                    scope, redirect_uri)
                return werkzeug.utils.redirect(permission_url)

        return "Hello, world"

    # generate token
    @http.route('/shopify/finalize/app', auth='public')
    def shopify_finalize_name(self, name, **kw):
        try:
            if 'shop' in kw:
                current_app = request.env.ref('app_external_id').sudo()
                if current_app:
                    shopify.Session.setup(
                        api_key=current_app.sp_api_key,
                        secret=current_app.sp_api_secret_key)
                    shopify_session = shopify.Session(kw['shop'], current_app.sp_api_version)
                    token = shopify_session.request_token(kw)
                    shopify.ShopifyResource.activate_session(shopify_session)
                    if token:
                        print(token)
                        # luu du lieu vao database here
                        #     1.check exist shop: neu co update, neu khong co tao moi
                        #     2.call API get shop info from shopify
                        #     3.store shop in database
                        #         create shop app
                        shop = request.env['s.sp.shop'].sudo().create({'#shop_data'})
                        shop_app = request.env['s.sp.app'].sudo().create({'#shop_app_data'})
                        #                 ...
                        # luu du lieu vao database end
                        # Cau 2: dang ki webhook
                        topic = 'order/create'
                        path = 'order/create/%s' % shop_app.shop_id.id
                        shop_app.add_webhook_to_shop(topic, path)
                        # Cau 3: Dang ki script tag
                        shop_app.add_script_tag_to_shop()
                        # 1: return "Hello, world"
                        # Cau 4: Tạo session login vào hệ  thống cho store
                        #         1. create user : check exist if not tao moi
                        letters = string.ascii_lowercase
                        password_generate = ''.join(random.choice(letters) for i in range(30))
                        current_company = http.request.env['res.company'].sudo().search([('name', '=', kw['shop'])],
                                                                                        limit=1)
                        # if not create company
                        user = request.env['user'].sudo().create({
                            'login': kw['shop'],
                            'password': password_generate,
                            'sp_shop_id': shop.id,
                            'company_ids': [[6, False, [current_company.id]]], 'company_id': current_company.id,
                        })
                        db = http.request.env.cr.dbname
                        request.env.cr.commit()
                        uid = request.session.authenticate(db, kw['shop'], password_generate)
                        main_menu = '#xml_menu'
                        redirectUrl = current_app.base_url + '/web?#menu_id=' + str(
                            main_menu)
                        return werkzeug.utils.redirect(redirectUrl)
        except Exception as ex:
            return werkzeug.utils.redirect('https://shopify.com/')
        return werkzeug.utils.redirect('https://shopify.com/')

    @http.route('/order/create/<int:shop_id>', auth='public')
    def webhook_order_create(self, shop_id):
        print(shop_id)
        shop = request.env['s.sp.app'].sudo().search([('shop_id','=', shop_id)], limnit=1)
        # xu ly logic webhook
        #    ...
        # xu ly logic webhook end
        return

    @http.route('/xero/authenticate/<int:shop_id>', auth='public')
    def xero_authenticate(self,shop_id):
        try:
            from ..models.auth import XeroAuth
            callback_url = '#base_url' + '/xero/authenticate'
            auth = XeroAuth(client_id='#client_id', client_secret='#client_secret',callback_uri=callback_url)
            auth.verify(request.httprequest.url)
            xero_token = json.dumps(auth.token)
            xero_shop = request.env['shopify.shop.xero'].search([('sp_shop_id','=',shop_id)])
            if xero_shop:
                xero_shop.xero_token = xero_token
            else:
                raise Exception('Shop not found')

            main_menu = '#xml_menu'
            redirectUrl = '#base_url' + '/web?#menu_id=' + str(
                main_menu)
            return werkzeug.utils.redirect(redirectUrl)
        except Exception as e:
            return e.__class__.__name__ + ': ' + str(e)

    @http.route('/xero/main', auth='user')
    def xero_main(self):
        xero_shop = request.env['shopify.shop.xero'].search([('sp_shop_id', '=', request.env.user.sp_shop_id)])
        # render ra giao dien app /static/app_front_end/pages/index.js de lam quen voi react json
        # code giao dien trong /static/app_front_end/pages/index.js de lam quen voi react js
        # dung webpack de compiler thanh file /static/src/js/xero_front_end.js de chay trong Odoo thong qua asset backend inherit
        return request.render('shopify_test_module.xero_main', {
            'shop_id': xero_shop.id
        })

    @http.route('/xero/sync/<int:shop_id>', auth='user')
    def xero_main(self, shop_id):
        xero_shop = request.env['shopify.shop.xero'].search([('sp_shop_id', '=', shop_id)])
        xero_shop.sync()