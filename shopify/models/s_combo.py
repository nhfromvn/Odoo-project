from odoo import fields, models, api


class SProducts(models.Model):
    _name = 's.combo'
    _description = 'Combo'
    _rec_name = 'name'
    priority = fields.Integer()
    name = fields.Char()
    is_percent = fields.Boolean()
    value = fields.Float()
    type_apply = fields.Boolean()
    store_id = fields.Many2one("s.store.info")
    product_condition = fields.Many2one("s.products")
    quantity_condition = fields.Integer()
    color = fields.Selection([('xanh', 'xanh'),
                                 ('do', 'do'),
                              ('vang', 'vang')],)
    position = fields.Selection([('below', 'below cart'),
                                 ('above', 'above cart')],
                                'Position', default='below')
