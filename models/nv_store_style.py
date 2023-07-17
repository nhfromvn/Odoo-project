from odoo import models, fields, api


class VariantStyle(models.Model):
    _name = 'nv.store.style'
    shop = fields.Many2one('nv.store')
    type = fields.Char(default='Square Swatch')
    selected_swatch_outer_border = fields.Char(default='#000000')
    selected_swatch_inner_border = fields.Char(default='#DDDDDD')
    selected_button_border = fields.Char(default='#292929')
    selected_button_swatch_border = fields.Char(default='#CFCFCF')
    selected_button_text_color = fields.Char(default='#FFFFFF')
    selected_button_background_color = fields.Char(default='#292929')
    animation = fields.Char(default='no effect')
    example_option = fields.Char()
    example_text_selected = fields.Char()
    example_text_unselected = fields.Char()
    example_image_url_selected = fields.Char()
    example_image_url_unselected = fields.Char()

    def get_style(self):
        val = {
            'type': self.type,
            'selected_swatch_outer_border': self.selected_swatch_outer_border,
            'selected_swatch_inner_border': self.selected_swatch_inner_border,
            'selected_button_border': self.selected_button_border,
            'selected_button_swatch_border': self.selected_button_swatch_border,
            'selected_button_text_color': self.selected_button_text_color,
            'selected_button_background_color': self.selected_button_background_color,
            'animation': self.animation,
            'example_option': self.example_option,
            'example_text_selected': self.example_text_selected,
            'example_text_unselected': self.example_text_unselected,
            'example_image_url_selected': self.example_image_url_selected,
            'example_image_url_unselected': self.example_image_url_unselected,

            'id': self.id,
        }
        return val
