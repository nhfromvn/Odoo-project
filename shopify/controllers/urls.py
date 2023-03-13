import json

from odoo import http
from odoo.http import request
import os
import jinja2

path = os.path.realpath(os.path.join(os.path.dirname(__file__), '../static/src/html'))
loader = jinja2.FileSystemLoader(path)
jinja_env = jinja2.Environment(loader=loader, autoescape=True)
jinja_env.filters["json"] = json.dumps


class Urls(http.Controller):

    @http.route('/shopify', auth='public', website=True)
    def index(self, **kw):
        template = jinja_env.get_template('index.html')
        res = template.render()
        return res

    @http.route('/shopify/webhook-register', auth='public')
    def sc_webhook(self, **kw):
        template = jinja_env.get_template('webhook-register.html')
        res = template.render()
        return res

    @http.route('/shopify/fetch-product', auth='public')
    def sc_product(self, **kw):
        template = jinja_env.get_template('fetch-product.html')
        res = template.render()
        return res
    @http.route('/shopify/fetch-order', auth='public')
    def sc_order(self, **kw):
        template = jinja_env.get_template('fetch-order.html')
        res = template.render()
        return res

    @http.route('/xero', auth='public')
    def sc_xero(self, **kw):
        template = jinja_env.get_template('xero.html')
        res = template.render()
        return res
    @http.route('/cart', auth='public')
    def sc_cart(self, **kw):
        template = jinja_env.get_template('cart.html')
        res = template.render()
        return res

    @http.route('/shopify/app-settings', auth='public')
    def sc_settings(self, **kw):
        template = jinja_env.get_template('settings.html')
        res = template.render()
        return res