from odoo import http
from odoo.http import request
from odoo.addons.website.controllers.main import Website
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.portal.controllers.portal import _build_url_w_params
from odoo.addons.website.controllers.main import QueryURL


# class BundlePage(http.Controller):
#     @http.route('/bundles', type='http', auth="public", website=True)
#     def _bundle(self, product_id):
#         print(product_id)
#         return request.render(
#             'bt_thuc_hanh.bundles', {
#                 'bundles': request.env['product.bundle'].search([]),
#                 'product_id': product_id})
#
#     @http.route('/bundles/<model("product.bundle"):bundle>/<int:product_id>', type='http', auth="user", website=True)
#     def _product_bunlde_detail(self, **kw):
#         print(kw)
#         product_id = kw.get('product_id')
#         bundle = kw.get('bundle')
#         return request.render(
#             'bt_thuc_hanh.bundle', {
#                 'bundle': bundle,
#                 'product_id' : product_id
#             })
#
#     @http.route('/bundle-update', type='http', auth="user", website=True)
#     def _add_bundle(self, **post):
#         print(post)
#         count = 0
#         bundle_id = post.get('bundle_id')
#         product_id = post.get('product_id')
#         bundles = request.env['product.bundle.reports'].search([])
#         for bundle in bundles:
#             count += 1
#         request.env['product.bundle.reports'].sudo().create({
#             'bundle_id': bundle_id,
#             'total_save' : count +1,
#             'product_id' : product_id
#         })
class InheritWebsiteSale(WebsiteSale):
    # @http.route(['/shop/<model("product.template"):product>'], type='http', auth="public", website=True, sitemap=True)
    # def product_detail(self, product, category='', search='', **kwargs):
    #     res = super(InheritWebsiteSale,self).product(self, product, category='', search='', **kwargs)
    #     print("hello")
    #     return res
    #
    # @http.route(['/shop/product/<model("product.template"):product>'], type='http', auth="public", website=True,
    #             sitemap=False)
    # def product_old(self, product, category='', search='', **kwargs):
    #     res = super(InheritWebsiteSale,self).old_product(self, product, category='', search='', **kwargs)
    #     print("abc")
    #     return res
    def _prepare_product_values(self, product, category, search, **kwargs):
        add_qty = int(kwargs.get('add_qty', 1))

        product_context = dict(request.env.context, quantity=add_qty,
                               active_id=product.id,
                               partner=request.env.user.partner_id)
        ProductCategory = request.env['product.public.category']

        if category:
            category = ProductCategory.browse(int(category)).exists()

        attrib_list = request.httprequest.args.getlist('attrib')
        min_price = request.params.get('min_price')
        max_price = request.params.get('max_price')
        attrib_values = [[int(x) for x in v.split("-")] for v in attrib_list if v]
        attrib_set = {v[1] for v in attrib_values}

        keep = QueryURL('/shop', category=category and category.id, search=search, attrib=attrib_list,
                        min_price=min_price, max_price=max_price)

        categs = ProductCategory.search([('parent_id', '=', False)])

        pricelist = request.website.get_current_pricelist()

        if not product_context.get('pricelist'):
            product_context['pricelist'] = pricelist.id
            product = product.with_context(product_context)

        # Needed to trigger the recently viewed product rpc
        view_track = request.website.viewref("website_sale.product").track
        bundles = request.env['product.bundle'].search([])

        return {
            'search': search,
            'category': category,
            'pricelist': pricelist,
            'attrib_values': attrib_values,
            'attrib_set': attrib_set,
            'keep': keep,
            'categories': categs,
            'main_object': product,
            'product': product,
            'add_qty': add_qty,
            'view_track': view_track,
            'bundles': bundles
        }

    @http.route(['/shop/<model("product.template"):product>'], type='http', auth="public", website=True, sitemap=True)
    def product(self, product, category='', search='', **kwargs):
        return request.render("website_sale.product", self._prepare_product_values(product, category, search, **kwargs))

    @http.route('/bundle-update/<int:bundle_id>/<int:product_id>', type='http', auth="user", website=True)
    def _add_bundle(self, **post):
        print(post)
        count = 0
        bundle_id = post.get('bundle_id')
        product_id = post.get('product_id')
        bundles = request.env['product.bundle.reports'].search([])
        for bundle in bundles:
            count += 1
        request.env['product.bundle.reports'].sudo().create({
            'bundle_id': bundle_id,
            'total_save': count + 1,
            'product_id': product_id
        })

