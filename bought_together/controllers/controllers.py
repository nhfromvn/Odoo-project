from odoo import http
from odoo.http import request


class BoughTogetherController(http.Controller):
    @http.route('/bought-together', auth='user')
    def render(self, **kw):
        return request.render('bought_together.bought_together')
