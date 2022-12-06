from odoo import http
from odoo.http import request
from odoo.addons.website.controllers.main import Website
class BundlePage(http.Controller):
    @http.route('/bundles', type='http', auth="public", website=True)
    def bundle(self, product_id):
        print(product_id)
        return request.render(
            'bt_thuc_hanh.bundles', {
                'bundles': request.env['product.bundle'].search([]),
                'product_id': product_id })

    @http.route('/bundles/<model("product.bundle"):bundle>', type='http', auth="user", website=True)
    def library_book_detail(self, bundle):
        return request.render(
            'bt_thuc_hanh.bundle', {
                'bundle': bundle,
            })

