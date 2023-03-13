# -*- coding: utf-8 -*-
# from odoo import http


# class MyModules(http.Controller):
#     @http.route('/my_modules/my_modules', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/my_modules/my_modules/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('my_modules.listing', {
#             'root': '/my_modules/my_modules',
#             'objects': http.request.env['my_modules.my_modules'].search([]),
#         })

#     @http.route('/my_modules/my_modules/objects/<model("my_modules.my_modules"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('my_modules.object', {
#             'object': obj
#         })
