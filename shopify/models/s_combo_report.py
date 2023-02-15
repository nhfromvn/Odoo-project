from odoo import fields, models, api


class SComboReport(models.Model):
    _name = 's.combo.report'
    _description = 'Report'
    _rec_name = 'combo_id'
    combo_id = fields.Many2one('s.combo')
    store_id = fields.Many2one('s.store.info')
    applied = fields.Float()
