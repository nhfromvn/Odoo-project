from odoo import http
from odoo.http import request
from odoo.addons.website.controllers.main import Website


class BundlePage(http.Controller):
    @http.route('/bundles', type='http', auth="public", website=True)
    def _bundle(self, product_id):
        print(product_id)
        return request.render(
            'bt_thuc_hanh.bundles', {
                'bundles': request.env['product.bundle'].search([]),
                'product_id': product_id})

    @http.route('/bundles/<model("product.bundle"):bundle>', type='http', auth="user", website=True)
    def _product_bunlde_detail(self, bundle):
        return request.render(
            'bt_thuc_hanh.bundle', {
                'bundle': bundle,
            })

    @http.route('/bundle-update', type='http', auth="user", website=True)
    def _add_bundle(self, **post):
        count = 0
        bundle_id = post.get('bundle_id')
        bundles = request.env['product.bundle.reports'].search([])
        for bundle in bundles:
            count += 1
        request.env['product.bundle.reports'].sudo().create({
            'bundle_id': bundle_id,
            'total_save' : count +1
        })
