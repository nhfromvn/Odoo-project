from odoo import fields, models, api


class SXeroConfig(models.TransientModel):
    _inherit = 'res.config.settings'

    api_key_xero = fields.Char()
    secret_key_xero = fields.Char()

    @api.model
    def get_values(self):
        res = super().get_values()
        params = self.env['ir.config_parameter'].sudo()
        res.update(
            api_key_xero=str(params.get_param('xero.api_key')),
            secret_key_xero=str(params.get_param('xero.secret_key')))
        return res

    def set_values(self):
        super().set_values()
        param = self.env['ir.config_parameter'].sudo()

        field_api_key = self.api_key_xero if self.api_key else False
        field_secret_key = self.secret_key_xero if self.secret_key else False

        param.set_param('xero.api_key', field_api_key)
        param.set_param('xero.secret_key', field_secret_key)
