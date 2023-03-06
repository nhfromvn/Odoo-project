# -*- coding: utf-8 -*-
# from odoo import http


# class MySales(http.Controller):
#     @http.route('/my_sales/my_sales', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/my_sales/my_sales/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('my_sales.listing', {
#             'root': '/my_sales/my_sales',
#             'objects': http.request.env['my_sales.my_sales'].search([]),
#         })

#     @http.route('/my_sales/my_sales/objects/<model("my_sales.my_sales"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('my_sales.object', {
#             'object': obj
#         })
