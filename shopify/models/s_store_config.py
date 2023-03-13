from odoo import fields, models, api


class SStoreConfig(models.TransientModel):
    _inherit = 'res.config.settings'

    api_key = fields.Char()
    secret_key = fields.Char()

    @api.model
    def get_values(self):
        res = super().get_values()
        params = self.env['ir.config_parameter'].sudo()
        res.update(
            api_key=str(params.get_param('shopify.api_key')),
            secret_key=str(params.get_param('shopify.secret_key')))
        return res

    def set_values(self):
        super().set_values()
        param = self.env['ir.config_parameter'].sudo()

        field_api_key = self.api_key if self.api_key else False
        field_secret_key = self.secret_key if self.secret_key else False

        param.set_param('shopify.api_key', field_api_key)
        param.set_param('shopify.secret_key', field_secret_key)
