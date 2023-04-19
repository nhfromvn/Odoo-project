# -*- coding: utf-8 -*-
# from odoo import http


# class Customaddons/instafeed(http.Controller):
#     @http.route('/customaddons/instafeed/customaddons/instafeed', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/customaddons/instafeed/customaddons/instafeed/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('customaddons/instafeed.listing', {
#             'root': '/customaddons/instafeed/customaddons/instafeed',
#             'objects': http.request.env['customaddons/instafeed.customaddons/instafeed'].search([]),
#         })

#     @http.route('/customaddons/instafeed/customaddons/instafeed/objects/<model("customaddons/instafeed.customaddons/instafeed"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('customaddons/instafeed.object', {
#             'object': obj
#         })
