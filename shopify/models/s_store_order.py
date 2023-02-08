from odoo import fields, models, api


class SStoreOrder(models.Model):
    _name = 's.store.orders'
    _rec_name = 'name'

    id_order = fields.Char()
    name = fields.Char()
    s_store_id = fields.Many2one("s.store.info")
    item_ids = fields.One2many("s.item.lines", "order_id")
    state = fields.Selection([('yet_sync', 'Yet Sync'), ('synced', 'Synced')], default='yet_sync')

class SItemLines(models.Model):
    _name = "s.item.lines"
    _rec_name = 'name'

    order_id = fields.Many2one("s.store.orders")
    product_id = fields.Char()
    name = fields.Char()
    id_item = fields.Char()
    price = fields.Float()
    quantity = fields.Integer()
