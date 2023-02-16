from odoo import fields, models, api


class SStoreOrder(models.Model):
    _name = 's.store.orders'
    _rec_name = 'name'

    id_order = fields.Char()
    name = fields.Char()
    s_store_id = fields.Many2one("s.store.info")
    item_ids = fields.One2many("s.item.lines", "order_id")
    state = fields.Selection([('yet_sync', 'Yet Sync'), ('synced', 'Synced')], default='yet_sync')
    financial_status = fields.Char()
    # total_price = fields.Float(compute="_compute_price")
    #
    # @api.depends("item_ids.price", "item_ids.quantity")
    # def _compute_price(self):
    #     self.total_price = 0
    #     for item in self.item_ids:
    #         self.total_price += item.quantity * item.price


class SItemLines(models.Model):
    _name = "s.item.lines"
    _rec_name = 'name'

    order_id = fields.Many2one("s.store.orders")
    product_id = fields.Char()
    name = fields.Char()
    id_item = fields.Char()
    price = fields.Float()
    quantity = fields.Integer()
