# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
class Instafeed(http.Controller):
    @http.route('/instafeed', auth='user')
    def index(self, **kw):
        return request.render('instafeed.instafeed')
    @http.route('/instafeed/error', auth='user')
    def connect_error(self, **kw):
        return ''' <b>This store already connect with other account
                Login to another account or change your connecting store to continue</b> '''

