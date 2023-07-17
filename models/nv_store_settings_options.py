from odoo import models, fields, api


class VariantOption(models.Model):
    _name = 'nv.store.settings.options'
    option_name = fields.Char()
    shop = fields.Many2one('nv.store')
    prevent_default = fields.Boolean(default=False)
    collection_page_swatch_image = fields.Char(default='Use 1st image of variant')
    product_page_swatch_image = fields.Char(default='Use 1st image of variant')
    product_style = fields.Many2one('nv.store.style')
    collection_style = fields.Many2one('nv.store.style')
    type = fields.Char(default='option_only')
    inventory_threshold = fields.Integer(default=10)
    notification_message = fields.Char(default='Only 10 left')
    option_label = fields.Char(default='Only 10 left')
    add_to_cart_label = fields.Char(default='Only 10 left')
    product_affected = fields.Integer(default=0)

    def get_option(self):
        vals = {
            'name': self.option_name,
            'product_affect': self.product_affected,
            'product_style': self.product_style.type,
            'collection_style': self.collection_style.type,
            'collection_page_swatch_image': self.collection_page_swatch_image,
            'product_page_swatch_image': self.product_page_swatch_image,
            'prevent_default': self.prevent_default
        }

        return vals
