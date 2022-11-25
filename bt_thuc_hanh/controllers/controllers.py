# -*- coding: utf-8 -*-
# from odoo import http


# class BtThucHanh(http.Controller):
#     @http.route('/bt_thuc_hanh/bt_thuc_hanh', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/bt_thuc_hanh/bt_thuc_hanh/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('bt_thuc_hanh.listing', {
#             'root': '/bt_thuc_hanh/bt_thuc_hanh',
#             'objects': http.request.env['bt_thuc_hanh.bt_thuc_hanh'].search([]),
#         })

#     @http.route('/bt_thuc_hanh/bt_thuc_hanh/objects/<model("bt_thuc_hanh.bt_thuc_hanh"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('bt_thuc_hanh.object', {
#             'object': obj
#         })
