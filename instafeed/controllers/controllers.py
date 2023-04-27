# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class Instafeed(http.Controller):
    @http.route('/instafeed', auth='user')
    def index(self, **kw):
        return request.render('instafeed.instafeed')



