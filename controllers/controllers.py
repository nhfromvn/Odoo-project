# -*- coding: utf-8 -*-

import json

from odoo import http
from odoo.http import request
from .auth import verify_request, is_limit_shop_request, is_shop_login, verify_app_proxy_request
from urllib.parse import urlencode, parse_qs
from urllib import parse


class KingVariantControllers(http.Controller):
    @http.route('/shopify/bundle/api', methods=['POST'], type='json', auth='public')
    def api(self, **kw):
        # verify_request()
        if not self.is_limit_shop_request() and self.is_shop_login(kw):
            return True
        return False

    @http.route('/king_variant/get_product', type="json", auth='public')
    # todo
    # tat ca cac api public deu phai verify request thong qua request params
    # tach tat cac cac api sang file controller khac, file nay chi co cac ham authen thoi

    def get_product(self, **kw):
        verify_request()
        # session = request.session
        if not is_limit_shop_request():
            shop_url = request.env['ir.config_parameter'].sudo().get_param('king.variant.shop_url')
            shop = request.env['nv.store'].sudo().search([('url', '=', shop_url)], limit=1)
            product = shop.get_product()
            print(product)
            return {'text': product}
        return False

    @http.route('/king_variant/get_data', type='json', auth='public')
    def get_data(self, **kw):
        verify_request()
        if not is_limit_shop_request():
            query = parse.urlsplit(request.httprequest.referrer).query
            dict_params = dict(parse_qs(query))
            params = {k: v[0] for k, v in dict_params.items()}
            shop_url = params['shop']
            shop = request.env['nv.store'].sudo().search([('url', '=', shop_url)], limit=1)
            variant_options = request.env['nv.store.settings.options'].sudo().search(
                [('shop', '=', shop.id), ('type', '=', 'option_only')])
            variant_styles = request.env['nv.store.style'].sudo().search(
                [('shop', '=', shop.id)])
            settings = request.env['nv.store.settings.options'].sudo().search(
                [('shop', '=', shop.id), ('type', '=', 'general')], limit=1)
            options = []
            styles = []
            themes = shop.get_themes()
            # todo
            # ham hoi lộn xộn, tách hàm get data của từng model riêng vào trong model.
            used_style = set()
            for variant_option in variant_options:
                options.append(variant_option.get_option())
                used_style.add(variant_option.product_style.type)
                used_style.add(variant_option.collection_style.type)
            for variant_style in variant_styles:
                # todo
                # dat ten bien cẩu thả quá, k đặt là 1, 2 gì cả, viết rõ ra first second hoặc nghĩ ra tên để phân biệt
                val = variant_style.get_style()
                val['in_use'] = True if variant_style.type in used_style else False,
                styles.append(val)
            # todo
            # return han json luon len front end dung luon chu
            return {'options': options,
                    'theme': themes,
                    'styles': styles, }
            # 'general': general}

        return False

    @http.route('/king_variant/save/option_data', auth='public', type='json')
    def save_option_data(self, **kwargs):
        verify_request()
        if not is_limit_shop_request():
            try:
                res = json.loads(request.httprequest.data)['params']
                query = parse.urlsplit(request.httprequest.referrer).query
                dict_params = dict(parse_qs(query))
                params = {k: v[0] for k, v in dict_params.items()}
                shop_url = params['shop']
                shop = request.env['nv.store'].sudo().search([('url', '=', shop_url)], limit=1)
                for option in res['options']:
                    variant_option = request.env['nv.store.settings.options'].sudo().search(
                        [('type', '=', 'option_only'), ('shop', '=', shop.id), ('option_name', '=', option['name'])],
                        limit=1)
                    variant_option.write({
                        'prevent_default': option['prevent_default'],
                        'product_page_swatch_image': option['product_page_swatch_image'],
                        'collection_page_swatch_image': option['collection_page_swatch_image'],
                        'collection_style': request.env['nv.store.style'].sudo().search(
                            [('shop', '=', shop.id), ('type', '=', option['collection_style'])]),
                        'product_style': request.env['nv.store.style'].sudo().search(
                            [('shop', '=', shop.id), ('type', '=', option['product_style'])]),
                    })
                # variant_settings = request.env['nv.store.settings.options'].sudo().search(
                #     [('type', '=', 'general'), ('shop', '=', shop.id)], limit=1)
                # variant_settings.write({
                #     'add_to_cart_label': res['general']['add_to_cart_label'],
                #     'inventory_threshold': res['general']['inventory_threshold'],
                #     'notification_message': res['general']['notification_message'],
                #     'option_label': res['general']['option_label'],
                # })
                return True
            except Exception as e:
                print(e)
                return False
        return False

    @http.route('/king_variant/save/theme', auth='public', type='json')
    def save_theme(self, **kwargs):
        verify_request()
        if not is_limit_shop_request():
            try:
                res = json.loads(request.httprequest.data)
                query = parse.urlsplit(request.httprequest.referrer).query
                dict_params = dict(parse_qs(query))
                params = {k: v[0] for k, v in dict_params.items()}
                shop_url = params['shop']
                shop = request.env['nv.store'].sudo().search([('url', '=', shop_url)], limit=1)
                for theme in res['themes']:
                    theme_exist = request.env['nv.theme.active'].sudo().search(
                        [('shop', '=', shop.id), ('theme_id', '=', theme['theme_id'])], limit=1)
                    theme_exist.write({
                        'is_active': theme['is_active']
                    })
                    if theme['is_active']:
                        shop.put_asset_theme(theme['theme_id'])
                    else:
                        shop.restore_theme(theme['theme_id'])
                print('haha')
                return True
            except Exception as e:
                print(e)
                return False
        return False

    @http.route('/king_variant/save/style', auth='public', type='json')
    def save_style(self, **kwargs):
        verify_request()
        if not is_limit_shop_request():
            try:
                res = json.loads(request.httprequest.data)['params']
                query = parse.urlsplit(request.httprequest.referrer).query
                dict_params = dict(parse_qs(query))
                params = {k: v[0] for k, v in dict_params.items()}
                shop_url = params['shop']
                shop = request.env['nv.store'].sudo().search([('url', '=', shop_url)], limit=1)
                print(res['type'])
                style = request.env['nv.store.style'].sudo().search(
                    [('shop', '=', shop.id), ('type', '=', res['type'])])
                print(style)
                style.write({
                    'selected_button_background_color': res['selected_button_background_color'],
                    'selected_button_border': res['selected_button_border'],
                    'selected_button_swatch_border': res['selected_button_swatch_border'],
                    'selected_button_text_color': res['selected_button_text_color'],
                    'selected_swatch_inner_border': res['selected_swatch_inner_border'],
                    'selected_swatch_outer_border': res['selected_swatch_outer_border'],
                    'animation': res['animation']
                })
                return res
            except Exception as e:
                print(e)
                return False
        return False

    @http.route('/king_variant/show', auth='public', type='json')
    def show(self, **kwargs):
        verify_app_proxy_request()
        if not is_limit_shop_request():
            try:
                res = json.loads(request.httprequest.data)
                shop_url = res['shop_url']
                shop = request.env['nv.store'].sudo().search([('url', '=', shop_url)], limit=1)
                print(res)
                variant_options = request.env['nv.store.settings.options'].sudo().search(
                    [('shop', '=', shop.id), ('type', '=', 'option_only')])
                variant_styles = request.env['nv.store.style'].sudo().search(
                    [('shop', '=', shop.id)])
                settings = request.env['nv.store.settings.options'].sudo().search(
                    [('shop', '=', shop.id), ('type', '=', 'general')], limit=1)
                general = {
                    'inventory_threshold': settings.inventory_threshold,
                    'notification_message': settings.notification_message,
                    'option_label': settings.option_label,
                    'add_to_cart_label': settings.add_to_cart_label
                }
                options = []
                button = {}
                swatch = {}
                swatch_in_pill = {}
                used_style = set()
                for variant_option in variant_options:
                    options.append(variant_option.get_option())
                    used_style.add(variant_option.product_style.type)
                    used_style.add(variant_option.collection_style.type)
                for variant_style in variant_styles:
                    style = variant_style.get_style()
                    style['in_use'] = True if variant_style.type in used_style else False,
                    if variant_style.type == 'Button':
                        button = style
                    if variant_style.type == 'Square swatch':
                        swatch = style
                    if variant_style.type == 'Swatch in pill':
                        swatch_in_pill = style
                styles = {
                    'button': button,
                    'swatch': swatch,
                    'swatch_in_pill': swatch_in_pill
                }
                products = shop.get_product()
                return {'options': options,
                        'styles': styles,
                        'general': general,
                        'products': products,
                        'res': res}
            except Exception as e:
                print(e)
                return False
        return False
