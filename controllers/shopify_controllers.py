# -*- coding: utf-8 -*-
import hashlib
import hmac
import json
import traceback
from datetime import datetime
from urllib import parse
from urllib.parse import urlencode
from odoo.tools import date_utils
from werkzeug.http import dump_cookie
from odoo.service import security

import shopify
import werkzeug

from odoo import http
from odoo.http import request, _logger, Response

SCOPES = ['read_products', 'read_themes']


class Root(http.Root):
    def get_response(self, httprequest, result, explicit_session):
        if isinstance(result, Response) and result.is_qweb:
            try:
                result.flatten()
            except Exception as e:
                if request.db:
                    result = request.registry['ir.http']._handle_exception(e)
                else:
                    raise

        if isinstance(result, (bytes, str)):
            response = Response(result, mimetype='text/html')
        else:
            response = result

        save_session = (not request.endpoint) or request.endpoint.routing.get('save_session', True)
        if not save_session:
            return response

        if httprequest.session.should_save:
            if httprequest.session.rotate:
                self.session_store.delete(httprequest.session)
                httprequest.session.sid = self.session_store.generate_key()
                if httprequest.session.uid:
                    httprequest.session.session_token = security.compute_session_token(httprequest.session, request.env)
                httprequest.session.modified = True
            self.session_store.save(httprequest.session)
        # We must not set the cookie if the session id was specified using a http header or a GET parameter.
        # There are two reasons to this:
        # - When using one of those two means we consider that we are overriding the cookie, which means creating a new
        #   session on top of an already existing session and we don't want to create a mess with the 'normal' session
        #   (the one using the cookie). That is a special feature of the Session Javascript class.
        # - It could allow session fixation attacks.
        if not explicit_session and hasattr(response, 'set_cookie'):
            cookie = dump_cookie('session_id', request.session.sid, max_age=90 * 24 * 60 * 60, secure=True,
                                 httponly=True)
            cookie = "{}; {}".format(cookie, b'SameSite=None'.decode('latin1'))
            response.headers.add('Set-Cookie', cookie)

        return response


http.Root.get_response = Root.get_response


class KingVariant(http.Controller):

    @http.route('/king_variant/install', auth='public')
    def index(self, **kw):
        if self.is_shop_auth(self, kw):
            # redirect_url = 'https://' + kw['shop'] + '/apps/shopify/main'
            redirect_url = '/king_variant?' + urlencode(request.params)
            return werkzeug.utils.redirect(redirect_url)
        # base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
        return werkzeug.utils.redirect("/king_variant/auth?" + urlencode(request.params))

    @staticmethod
    def expire_session(timestamp):
        # todo
        current_timestamp = datetime.now().timestamp()
        timestamp = current_timestamp
        dt_obj = datetime.fromtimestamp(timestamp)
        print(dt_obj)
        # check last shop last login by field last_login in shop, > 30p return False
        return False

    @staticmethod
    def is_shop_auth(self, kw):
        shop_url = kw['shop']
        timestamp = kw['timestamp']
        shop = request.env['shopify.shop'].sudo().search([('url', '=', shop_url)], limit=1)
        if shop and not self.expire_session(timestamp):
            return True
        return False

    @staticmethod
    def is_shop_login(kw):
        shop_url = kw['shop']
        is_shop_login = 'king_variant' in request.session and request.session['is_shop_login'] == shop_url
        print(is_shop_login)
        return is_shop_login

    @http.route('/king_variant/auth', auth='public')
    def install(self, **kw):
        if 'shop' in kw:
            store_url = kw.get('shop').replace('https://', '').replace('http://', '').split('/')[0]
            api_key = request.env['ir.config_parameter'].sudo().get_param('king.variant.api_key_king_variant')
            secret_key = request.env['ir.config_parameter'].sudo().get_param('king.variant.secret_key_king_variant')
            api_version = request.env['ir.config_parameter'].sudo().get_param('king.variant.api_version_king_variant')
            base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
            shopify.ShopifyResource.clear_session()
            shopify.Session.setup(
                api_key=api_key,
                secret=secret_key)
            shopify_session = shopify.Session(store_url, api_version)
            scope = SCOPES
            redirect_uri = base_url + "/king_variant/oauth/callback"
            permission_url = shopify_session.create_permission_url(
                scope, redirect_uri)
            return werkzeug.utils.redirect(permission_url)
        return "Hello, world"

    @http.route('/king_variant/oauth/callback', auth='public')
    def finalize(self, **kw):
        if 'shop' not in request.params:
            raise Exception('Missing shop url parameter')
        # shop = request.params['shop']
        api_key = request.env['ir.config_parameter'].sudo().get_param('king.variant.api_key_king_variant')
        secret_key = request.env['ir.config_parameter'].sudo().get_param('king.variant.secret_key_king_variant')
        api_version = request.env['ir.config_parameter'].sudo().get_param('king.variant.api_version_king_variant')
        try:
            shopify.Session.setup(
                api_key=api_key,
                secret=secret_key)
            shopify_session = shopify.Session(kw['shop'], api_version)
            token = shopify_session.request_token(kw)
            shop = request.env['shopify.shop'].sudo().search([('url', '=', kw['shop'])], limit=1)
            if not shop:
                shop = request.env['shopify.shop'].sudo().create({
                    'url': kw['shop'],
                    'access_token': token
                })
            else:
                shop.access_token = token
            shop.get_themes()
            request.session['king_variant'] = kw['shop']
            redirect_url = 'https://' + kw['shop'] + '/admin/apps/' + api_key
            return werkzeug.utils.redirect(redirect_url)

        except Exception as e:
            _logger.error(traceback.format_exc())
        return "Hello, world"

    @http.route('/king_variant', auth='public')
    def main(self, **kw):
        self.verify_request()
        headers = {
            'Content-Security-Policy': "frame-ancestors " + "https://hoangnam3.myshopify.com" + " https://admin.shopify.com;"}
        return request.render('king_variant.index', {}, headers=headers)

    @http.route('/shopify/bundle/api', methods=['POST'], type='json', auth='public')
    def api(self, **kw):
        self.verify_request()
        if not self.is_limit_shop_request() and self.is_shop_login(kw):
            return True
        return False

    @http.route('/king_variant/get_product', auth='public')
    def get_product(self, **kw):
        shop_url = request.env['ir.config_parameter'].sudo().get_param('king.variant.shop_url')
        shop = request.env['shopify.shop'].sudo().search([('url', '=', shop_url)], limit=1)
        product = shop.get_product()
        print(product)
        return json.dumps({'text': product})

    @http.route('/king_variant/get_data', auth='public')
    def get_data(self, **kw):
        shop_url = request.env['ir.config_parameter'].sudo().get_param('king.variant.shop_url')
        shop = request.env['shopify.shop'].sudo().search([('url', '=', shop_url)], limit=1)
        variant_options = request.env['variant.option'].sudo().search(
            [('shop', '=', shop.id), ('type', '=', 'option_only')])
        options = []
        themes = []
        shop.get_themes()
        for theme in shop.themes:
            themes.append(
                {'theme_id': theme.theme_id}
            )
        for variant_option in variant_options:
            options.append({
                'name': variant_option.option_name,
                'product_affect': variant_option.product_affected,
            })
        return json.dumps({'option': options,
                           'theme': themes})

    @staticmethod
    def is_limit_shop_request():
        # todo
        # luu recent timestamp request to shop, now - timestamp < 3 return true
        return False

    @staticmethod
    def verify_request():
        try:
            secret_key = request.env['ir.config_parameter'].sudo().get_param('king.variant.secret_key_king_variant')
            shopify.Session.secret = secret_key
            params = request.params
            if 'data' in params:
                del params['data']
            params['hmac'] = params['hmac']
            hmac = shopify.Session.calculate_hmac(params)
            if params['hmac'] != hmac:
                raise Exception("Unauthorized request")
            return True
        except Exception as e:
            _logger.error(traceback.format_exc())
            raise Exception("Error")

    @staticmethod
    def verify_app_proxy_request():
        # use for request on store front end
        secret_key = request.env['ir.config_parameter'].sudo().get_param('king.variant.secret_key_king_variant')
        query_params = dict(parse.parse_qs(request.httprequest.query_string))
        params = {key.decode('utf-8'): value[0].decode('utf-8') for (key, value) in query_params.items() if
                  key.decode('utf-8') != 'signature'}
        if 'logged_in_customer_id' not in params:
            params['logged_in_customer_id'] = ""

        def encoded_params(params):
            encoded_params = ''
            for key in sorted(params):
                encoded_params += key + '=' + params[key]
            return encoded_params

        hexdigest = hmac.new(
            secret_key.encode('utf-8'),
            encoded_params(params).encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        if not hmac.compare_digest(hexdigest.encode('utf-8'), query_params['signature'.encode('utf-8')][0]):
            _logger.error('Secret key is not verified.' + json.dumps(request.params))
            raise Exception('Secret key is not verified')
        return True
