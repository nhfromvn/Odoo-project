from odoo import models, fields, api
import shopify
from odoo.http import request


class ShopifyShop(models.Model):
    # todo
    # a ve database dat ten hộ cho bảng rồi vào đây lại sửa lại tên bảng
    _name = 'shopify.shop'
    shop_name = fields.Char()
    access_token = fields.Char()
    status = fields.Boolean()
    url = fields.Char()
    shop_id = fields.Char()
    variant_options = fields.One2many('variant.option', 'shop')
    themes = fields.One2many('shopify.theme', 'shop')
    last_login = fields.Float()
    recent_timestamp = fields.Datetime()

    def put_asset_theme(self, theme_id):
        # todo
        # chuyen qua dung theme extension 3.0, tao app block
        new_session = shopify.Session(self.url, request.env['ir.config_parameter'].sudo().get_param(
            'king.variant.api_version_king_variant'),
                                      token=self.access_token)
        shopify.ShopifyResource.activate_session(new_session)
        asset = shopify.Asset.create({
            "theme_id": theme_id,
            "key": "snippets/card-product.liquid",
            "src": "/king_variant/static/liquid/card-product.liquid"
        })
        asset = shopify.Asset.create({
            "theme_id": theme_id,
            "key": "snippets/product-variant-options.liquid",
            "src": "/king_variant/static/liquid/product-variant-options.liquid"
        })
        print(asset)

    def restore_theme(self, theme_id):
        new_session = shopify.Session(self.url, request.env['ir.config_parameter'].sudo().get_param(
            'king.variant.api_version_king_variant'),
                                      token=self.access_token)
        shopify.ShopifyResource.activate_session(new_session)
        asset = shopify.Asset.create({
            "theme_id": theme_id,
            "key": "snippets/card-product.liquid",
            "src": "/king_variant/static/liquid/card-product-restore.liquid"
        })
        asset = shopify.Asset.create({
            "theme_id": theme_id,
            "key": "snippets/product-variant-options.liquid",
            "src": "/king_variant/static/liquid/product-variant-options-restore .liquid"
        })
        print(asset)

    def script_tags_register(self):
        new_session = shopify.Session(self.url, request.env['ir.config_parameter'].sudo().get_param(
            'king.variant.api_version_king_variant'),
                                      token=self.access_token)
        shopify.ShopifyResource.activate_session(new_session)
        existing_script_tags = shopify.ScriptTag.find()
        base_url = request.env['ir.config_parameter'].sudo().get_param(
            'web.base.url')
        new_script_tag_url = f'{base_url}/king_variant/static/js/extension.js?v=8'
        new_script_tag = ''
        try:
            if existing_script_tags:
                for script_tag in existing_script_tags:
                    if script_tag.src != new_script_tag_url:
                        shopify.ScriptTag.find(script_tag.id).destroy()
                        new_script_tag = shopify.ScriptTag.create({
                            "event": "onload",
                            "src": new_script_tag_url
                        })
            else:
                new_script_tag = shopify.ScriptTag.create({
                    "event": "onload",
                    "src": new_script_tag_url
                })
                print(new_script_tag)
        except Exception as e:
            print(e)

    def get_themes(self):
        new_session = shopify.Session(self.url, request.env['ir.config_parameter'].sudo().get_param(
            'king.variant.api_version_king_variant'),
                                      token=self.access_token)
        shopify.ShopifyResource.activate_session(new_session)
        themes = shopify.Theme.find()

        for theme in themes:
            theme_exist = request.env['shopify.theme'].sudo().search(
                [('shop', '=', self.id), ('theme_id', '=', theme.id)], limit=1)
            if not theme_exist:
                request.env['shopify.theme'].sudo().create({
                    'shop': self.id,
                    'theme_id': str(theme.id),
                    'theme_name': theme.name,
                    'role': theme.role,
                    'is_active': True,
                })
            else:
                theme_exist.write({
                    'role': theme.role,
                    'theme_name': theme.name,
                })

    def get_product(self):
        # todo
        # viet ham active shopify session cho shop rieng ra de dung o tat cac cac cho khac, k viet lai code ntn
        new_session = shopify.Session(self.url, request.env['ir.config_parameter'].sudo().get_param(
            'king.variant.api_version_king_variant'),
                                      token=self.access_token)
        shopify.ShopifyResource.activate_session(new_session)
        products = shopify.Product.find()
        existing_script_tags = shopify.ScriptTag.find()
        vals = []
        # todo
        # giai thich a cong dung ham nay
        setting = request.env['variant.option'].sudo().search([('shop', '=', self.id), ('type', '=', 'general')])
        if not setting:
            request.env['variant.option'].sudo().create({
                'type': 'general',
                'shop': self.id
            })
        for type in [{'type': 'Square swatch',
                      'option': 'Color',
                      'image_url1': '/king_variant/static/images/example.jpg',
                      'image_url2': '/king_variant/static/images/Anh-meo-cute-dang-yeu-de-thuong.jpg',
                      }, {'type': 'Swatch in pill',
                          'option': 'Color',
                          'image_url1': '/king_variant/static/images/example.jpg',
                          'image_url2': '/king_variant/static/images/Anh-meo-cute-dang-yeu-de-thuong.jpg',
                          'text1': 'Red',
                          'text2': 'Blue'
                          }, {'type': 'Button',
                              'text1': 'Large',
                              'text2': 'Small',
                              'option': 'Size',
                              }]:
            style = request.env['variant.style'].sudo().search(
                [('shop', '=', self.id),
                 ('type', '=', type['type'])],
                limit=1)
            if not style:
                request.env['variant.style'].sudo().create({
                    'shop': self.id,
                    'type': type['type'],
                    'example_option': type['option'],
                    'example_text1': type['text1'] if 'text1' in type else False,
                    'example_text2': type['text2'] if 'text2' in type else False,
                    'example_image_url1': type['image_url1'] if 'image_url1' in type else False,
                    'example_image_url2': type['image_url2'] if 'image_url2' in type else False
                })
        square_swatch_id = request.env['variant.style'].sudo().search([('type', '=', 'Square swatch')], limit=1).id
        variant_options = request.env['variant.option'].sudo().search([('shop', '=', self.id)])
        for variant_option in variant_options:
            variant_option.product_affected = 0
        for product in products:
            options = []
            for option in product.options:
                list_values = []
                for option_value in option.values:
                    image_id = product.image.id if product.image else 0
                    for variant in product.variants:
                        if option_value == variant.option1 or option_value == variant.option2 or option_value == variant.option3:
                            if variant.image_id:
                                image_id = variant.image_id
                                break
                    flag = False
                    for image in product.images:
                        if image.id == image_id:
                            url = image.src
                            flag = True
                    if flag:
                        list_values.append({
                            'name': option_value,
                            'image_url': url
                        })
                    else:
                        list_values.append({
                            'name': option_value,
                        })
                options.append({
                    'id': option.id,
                    'name': option.name,
                    'values': list_values,
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
                            'product_affected': 1,
                            'type': 'option_only',
                            'product_style': square_swatch_id,
                            'collection_style': square_swatch_id
                        })
                    else:
                        variant_option.product_affected += 1
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
        # todo
        # không dc code ntn parameter là cố định, k thay đổi, k có parameter shop_url, parameter phải tự điền bằng tay
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
