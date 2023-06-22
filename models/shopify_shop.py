from odoo import models, fields, api
import shopify
from odoo.http import request


class ShopifyShop(models.Model):
    _name = 'shopify.shop'
    shop_name = fields.Char()
    access_token = fields.Char()
    status = fields.Boolean()
    url = fields.Char()
    shop_id = fields.Char()
    variant_options = fields.One2many('variant.option', 'shop')
    themes = fields.One2many('shopify.theme', 'shop')

    def get_themes(self):
        new_session = shopify.Session(self.url, request.env['ir.config_parameter'].sudo().get_param(
            'instafeed.api_version_instafeed'),
                                      token=self.access_token)
        shopify.ShopifyResource.activate_session(new_session)
        themes = shopify.Theme.find()
        for theme in themes:
            theme_exist = request.env['shopify.theme'].sudo().search(
                [('shop', '=', self.id), ('theme_id', '=', theme.id)], limit=1)
            if not theme_exist:
                request.env['shopify.theme'].sudo().create({
                    'shop': self.id,
                    'theme_id': str(theme.id)
                })

    def get_product(self):
        new_session = shopify.Session(self.url, request.env['ir.config_parameter'].sudo().get_param(
            'instafeed.api_version_instafeed'),
                                      token=self.access_token)
        shopify.ShopifyResource.activate_session(new_session)
        products = shopify.Product.find()
        vals = []
        variant_options = request.env['variant.option'].sudo().search([('shop', '=', self.id)])
        for variant_option in variant_options:
            variant_option.product_affected = 0
        for product in products:
            options = []
            for option in product.options:
                options.append({
                    'id': option.id,
                    'name': option.name,
                    'values': option.values,
                    'product_id': option.product_id,
                })
                if len(option.values) > 1:
                    variant_option = request.env['variant.option'].sudo().search(
                        [('shop', '=', self.id), ('option_name', '=', option.name), ('type', '=', 'option_only')],
                        limit=1)
                    if not variant_option:
                        variant_option = request.env['variant.option'].sudo().create({
                            'option_name': option.name,
                            'shop': self.id,
                            'product_affected': 1
                        })
                    else:
                        variant_option.product_affected += 1
                    for type in ['Square swatch', 'Square in pill', 'Button']:
                        style_collection = request.env['variant.style'].sudo().search(
                            [('shop', '=', self.id), ('variant_option_collection', '=', variant_option.id),
                             ('type', '=', type)],
                            limit=1)
                        if not style_collection:
                            request.env['variant.style'].sudo().create({
                                'shop': self.id,
                                'variant_option_collection': variant_option.id,
                                'type': type
                            })
                        style_product = request.env['variant.style'].sudo().search(
                            [('shop', '=', self.id), ('variant_option_product', '=', variant_option.id),
                             ('type', '=', type)],
                            limit=1)
                        if not style_product:
                            request.env['variant.style'].sudo().create({
                                'shop': self.id,
                                'variant_option_product': variant_option.id,
                                'type': type
                            })

            vals.append({
                'options': options,
                'product_id': product.id,
                'name': product.title,
                'url': f'{self.url}/products/{product.handle}',
                'shop_id': self.id,
                'price': float(product.variants[0].price),
                "compare_at_price": product.variants[0].compare_at_price,
                'qty': product.variants[0].inventory_quantity,
                "variant_id": product.variants[0].id,
                'image_url': product.image.src if product.image else None
            })
        return vals


class KingVariantConfig(models.TransientModel):
    _inherit = 'res.config.settings'
    api_key_king_variant = fields.Char()
    secret_key_king_variant = fields.Char()
    api_version_king_variant = fields.Char()
    shop_url = fields.Char()

    @api.model
    def get_values(self):
        res = super().get_values()
        params = self.env['ir.config_parameter'].sudo()
        res.update(
            shop_url=str(params.get_param('king.variant.shop_url')),
            api_key_king_variant=str(params.get_param('king.variant.api_key_king_variant')),
            secret_key_king_variant=str(params.get_param('king.variant.secret_key_king_variant')),
            api_version_king_variant=str(params.get_param('king.variant.api_version_king_variant'))
        )
        return res

    def set_values(self):
        super().set_values()
        param = self.env['ir.config_parameter'].sudo()
        shop_url = self.shop_url if self.shop_url else False
        api_key_king_variant = self.api_key_king_variant if self.api_key_king_variant else False
        secret_key_king_variant = self.secret_key_king_variant if self.secret_key_king_variant else False
        api_version_king_variant = self.api_version_king_variant if self.api_version_king_variant else False
        param.set_param('king.variant.api_key_king_variant', api_key_king_variant)
        param.set_param('king.variant.secret_key_king_variant', secret_key_king_variant)
        param.set_param('king.variant.api_version_king_variant', api_version_king_variant)
        param.set_param('king.variant.shop_url', shop_url)
