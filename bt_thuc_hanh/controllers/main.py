from odoo import http
from odoo.http import request
from odoo.addons.website.controllers.main import Website
from odoo.addons.website_sale.controllers.main import WebsiteSale
from odoo.addons.portal.controllers.portal import _build_url_w_params
from odoo.addons.website.controllers.main import QueryURL
from odoo import fields
from odoo.tools.json import scriptsafe as json_scriptsafe
from werkzeug.exceptions import Forbidden, NotFound


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
    def _find_best_bundle(self, bundles, order, **kwargs):
        list = []
        for bundle in bundles:
            list.append(bundle.priority)
        for bundle in bundles:
            if list:
                if bundle.priority == min(list):
                    best_bundle = bundle
        lines = order.order_line
        for line in lines:
            for bundle in bundles:
                if line.product_id in bundle.products.product_id:
                    if line.product_uom_qty <= 0:
                        self._find_best_bundle(bundles.remove(best_bundle))
                        if not bundles: best_bundle = False

        return best_bundle

    def _find_valid_bundle(self, bundles, order, **kwargs):
        lines = order.order_line
        bundles_valid = []
        for bundle in bundles:
            bundles_valid.append(bundle)
            if bundle.type == 'bundle':
                for bundle_product in bundle.products:
                    if bundle_product.product_id:
                        if bundle_product.product_id not in lines.product_id:
                            bundles_valid.remove(bundle)
                            break
            else:
                if bundle.product2 not in lines.product_id:
                    bundles_valid.remove(bundle)
        return bundles_valid

    def _compute_total_price(self, bundles, best_bundle, order, **kwargs):
        lines = order.order_line
        for line in lines:
            if best_bundle.type == 'bundle':
                list2 = []
                for line in lines:
                    for bundle_product in best_bundle.products:
                        if bundle_product.product_id.id == line.product_id.id:
                            remainder = line.product_uom_qty % bundle_product.quantity
                            list2.append(line.product_uom_qty // bundle_product.quantity)
                amount_bundle = min(list2)
                for line in lines:
                    for bundle_product in best_bundle.products:
                        if bundle_product.product_id.id == line.product_id.id:
                            line.qty_in_bundle = bundle_product.quantity * amount_bundle
                            line.qty_not_in_bundle = line.product_uom_qty - line.qty_in_bundle
                total_price = 0
                total_not_in_bundle_price1 = 0
                for line in lines:
                    total_not_in_bundle_price1 += line.product_id.list_price * line.qty_not_in_bundle
                total_not_in_bundle_price2 = 0
                for line in lines:
                    if line.product_id not in best_bundle.products.product_id:
                        total_not_in_bundle_price2 = + line.product_id.list_price * line.product_uom_qty
                total_price = total_not_in_bundle_price1 + total_not_in_bundle_price2 + best_bundle.total_price * amount_bundle
        return total_price


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
        bundles = request.env['product.bundle'].search(
            ['|', ('products.product_id.product_tmpl_id.id', '=', product.id),
             ('product2.product_tmpl_id.id', '=', product.id)])
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

    # @http.route(['/shop/cart/update'], type='http', auth="public", methods=['POST'], website=True)
    # def cart_update(self, product_id, add_qty=1, set_qty=0, **kw):
    #     """This route is called when adding a product to cart (no options)."""
    #     sale_order = request.website.sale_get_order(force_create=True)
    #     if sale_order.state != 'draft':
    #         request.session['sale_order_id'] = None
    #         sale_order = request.website.sale_get_order(force_create=True)
    #
    #     product_custom_attribute_values = None
    #     if kw.get('product_custom_attribute_values'):
    #         product_custom_attribute_values = json_scriptsafe.loads(kw.get('product_custom_attribute_values'))
    #
    #     no_variant_attribute_values = None
    #     if kw.get('no_variant_attribute_values'):
    #         no_variant_attribute_values = json_scriptsafe.loads(kw.get('no_variant_attribute_values'))
    #
    #     sale_order._cart_update(
    #         product_id=int(product_id),
    #         add_qty=add_qty,
    #         set_qty=set_qty,
    #         product_custom_attribute_values=product_custom_attribute_values,
    #         no_variant_attribute_values=no_variant_attribute_values
    #     )
    #
    #     if kw.get('express'):
    #         return request.redirect("/shop/checkout?express=1")
    #
    #     return request.redirect("/shop/cart")
    #
    # @http.route(['/shop/cart/update_json'], type='json', auth="public", methods=['POST'], website=True, csrf=False)
    # def cart_update_json(self, product_id, line_id=None, add_qty=None, set_qty=None, display=True, **kw):
    #     """
    #     This route is called :
    #         - When changing quantity from the cart.
    #         - When adding a product from the wishlist.
    #         - When adding a product to cart on the same page (without redirection).
    #     """
    #     order = request.website.sale_get_order(force_create=1)
    #     if order.state != 'draft':
    #         request.website.sale_reset()
    #         if kw.get('force_create'):
    #             order = request.website.sale_get_order(force_create=1)
    #         else:
    #             return {}
    #
    #     pcav = kw.get('product_custom_attribute_values')
    #     nvav = kw.get('no_variant_attribute_values')
    #     value = order._cart_update(
    #         product_id=product_id,
    #         line_id=line_id,
    #         add_qty=add_qty,
    #         set_qty=set_qty,
    #         product_custom_attribute_values=json_scriptsafe.loads(pcav) if pcav else None,
    #         no_variant_attribute_values=json_scriptsafe.loads(nvav) if nvav else None
    #     )
    #
    #     if not order.cart_quantity:
    #         request.website.sale_reset()
    #         return value
    #
    #     order = request.website.sale_get_order()
    #     value['cart_quantity'] = order.cart_quantity
    #
    #     if not display:
    #         return value
    #
    #     value['website_sale.cart_lines'] = request.env['ir.ui.view']._render_template("website_sale.cart_lines", {
    #         'website_sale_order': order,
    #         'date': fields.Date.today(),
    #         'suggested_products': order._cart_accessories()
    #     })
    #     value['website_sale.short_cart_summary'] = request.env['ir.ui.view']._render_template("website_sale.short_cart_summary", {
    #         'website_sale_order': order,
    #     })
    #     return value

    @http.route(['/shop/cart'], type='http', auth="public", website=True, sitemap=False)
    def cart(self, access_token=None, revive='', **post):
        """
        Main cart management + abandoned cart revival
        access_token: Abandoned cart SO access token
        revive: Revival method when abandoned cart. Can be 'merge' or 'squash'
        """
        order = request.website.sale_get_order()
        bundles = request.env['product.bundle'].search([])
        bundle_valid = self._find_valid_bundle(bundles,order)
        best_bundle = self._find_best_bundle(bundle_valid,order)
        order.amount_untaxed = self._compute_total_price(bundles, best_bundle, order)
        if order and order.state != 'draft':
            request.session['sale_order_id'] = None
            order = request.website.sale_get_order()
        values = {}
        if access_token:
            abandoned_order = request.env['sale.order'].sudo().search([('access_token', '=', access_token)], limit=1)
            if not abandoned_order:  # wrong token (or SO has been deleted)
                raise NotFound()
            if abandoned_order.state != 'draft':  # abandoned cart already finished
                values.update({'abandoned_proceed': True})
            elif revive == 'squash' or (revive == 'merge' and not request.session.get(
                    'sale_order_id')):  # restore old cart or merge with unexistant
                request.session['sale_order_id'] = abandoned_order.id
                return request.redirect('/shop/cart')
            elif revive == 'merge':
                abandoned_order.order_line.write({'order_id': request.session['sale_order_id']})
                abandoned_order.action_cancel()
            elif abandoned_order.id != request.session.get(
                    'sale_order_id'):  # abandoned cart found, user have to choose what to do
                values.update({'access_token': abandoned_order.access_token})

        values.update({
            'website_sale_order': order,
            'date': fields.Date.today(),
            'suggested_products': [],
            'bundles': bundles
        })
        if order:
            order.order_line.filtered(lambda l: not l.product_id.active).unlink()
            _order = order
            if not request.env.context.get('pricelist'):
                _order = order.with_context(pricelist=order.pricelist_id.id)
            values['suggested_products'] = _order._cart_accessories()
        if post.get('type') == 'popover':
            # force no-cache so IE11 doesn't cache this XHR
            return request.render("website_sale.cart_popover", values, headers={'Cache-Control': 'no-cache'})
        return request.render("website_sale.cart", values)

    @http.route(['/shop/<model("product.template"):product>'], type='http', auth="public", website=True, sitemap=True)
    def product(self, product, category='', search='', **kwargs):
        return request.render("website_sale.product", self._prepare_product_values(product, category, search, **kwargs))

    @http.route("/bundle-update/<model('product.bundle'):bundle>/<int:product_id>", type='http', auth="user",
                website=True)
    def _add_bundle(self, **post):
        count = 0
        bundle = post.get('bundle')
        bundle_id = bundle.id
        product_id = post.get('product_id')
        sale_order = request.website.sale_get_order(force_create=True)
        request.website.sale_reset()
        # sale_order.write({'order_line': [(5, 0, 0)]})
        reports = request.env['product.bundle.reports'].search([])
        for product in bundle.products:
            sale_order._cart_update(product_id=product.product_id.id, line_id=None, add_qty=product.quantity,
                                    set_qty=None)
        for report in reports:
            count += 1

        request.env['product.bundle.reports'].sudo().create({
            'bundle_id': bundle_id,
            'save_id': count + 1,
            'product_id': product_id,
            'sale_id': sale_order.id
        })
        return request.redirect("/shop/cart")

    @http.route(['/shop/cart/update_json'], type='json', auth="public", methods=['POST'], website=True, csrf=False)
    def cart_update_json(self, product_id, line_id=None, add_qty=None, set_qty=None, display=True, **kw):
        """
        This route is called :
            - When changing quantity from the cart.
            - When adding a product from the wishlist.
            - When adding a product to cart on the same page (without redirection).
        """
        order = request.website.sale_get_order(force_create=1)
        if order.state != 'draft':
            request.website.sale_reset()
            if kw.get('force_create'):
                order = request.website.sale_get_order(force_create=1)
            else:
                return {}
        pcav = kw.get('product_custom_attribute_values')
        nvav = kw.get('no_variant_attribute_values')
        value = order._cart_update(
            product_id=product_id,
            line_id=line_id,
            add_qty=add_qty,
            set_qty=set_qty,
            product_custom_attribute_values=json_scriptsafe.loads(pcav) if pcav else None,
            no_variant_attribute_values=json_scriptsafe.loads(nvav) if nvav else None
        )

        if not order.cart_quantity:
            request.website.sale_reset()
            return value

        order = request.website.sale_get_order()
        bundles = request.env['product.bundle'].search([])
        list = []
        for bundle in bundles:
            list.append(bundle.priority)
        for bundle in bundles:
            if list:
                if bundle.priority == min(list):
                    best_bundle = bundle
        order.amount_untaxed = self._compute_total_price(bundles, best_bundle, order)
        value['cart_quantity'] = order.cart_quantity

        if not display:
            return value

        value['website_sale.cart_lines'] = request.env['ir.ui.view']._render_template("website_sale.cart_lines", {
            'website_sale_order': order,
            'date': fields.Date.today(),
            'suggested_products': order._cart_accessories()
        })
        value['website_sale.short_cart_summary'] = request.env['ir.ui.view']._render_template(
            "website_sale.short_cart_summary", {
                'website_sale_order': order,
            })
        return value
