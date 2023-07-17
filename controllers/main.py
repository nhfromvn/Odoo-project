# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request, _logger, Response
from .auth import verify_request

class KingVariantIndex(http.Controller):
    @http.route('/king_variant', auth='public')
    def main(self, **kw):
        # todo
        # shop url lay tu request params
        shop_url = request.params['shop']
        verify_request()
        headers = {
            'Content-Security-Policy': "frame-ancestors " + shop_url + " https://admin.shopify.com;"}
        return request.render('king_variant.index', {}, headers=headers)
