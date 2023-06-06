from odoo import models, fields, api, _
import shopify
from odoo.http import request
from odoo.exceptions import ValidationError


class ShopifyStore(models.Model):
    _name = 'shopify.store'
    shop_name = fields.Char()
    name = fields.Char()
    email = fields.Char()
    is_delete = fields.Boolean()
    timezone = fields.Boolean()
    access_token = fields.Char()
    admin = fields.Many2one('res.users')
    shop_id = fields.Char()
    currency = fields.Char()
    status = fields.Boolean()
    url = fields.Char()
    country = fields.Char()
    password = fields.Char()
    is_update_script_tag = fields.Boolean()
    shopify_owner = fields.Char()

    def get_product(self):
        new_session = shopify.Session(self.url, request.env['ir.config_parameter'].sudo().get_param(
            'instafeed.api_version_instafeed'),
                                      token=self.access_token)
        shopify.ShopifyResource.activate_session(new_session)
        products = shopify.Product.find()
        vals = []
        for product in products:
            vals.append({
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

    def change_script_tag_url(self):
        try:
            print("start cron job change_script_tag!")
            old_shops = self.env['shopify.store'].sudo().search([('is_update_script_tag', '=', False)], limit=10)
            shopify_api_version = self.env['ir.config_parameter'].sudo().get_param('instafeed.api_version_instafeed')
            for shop in old_shops:
                new_session = shopify.Session(token=shop.access_token, shop_url=shop.url, version=shopify_api_version)
                shopify.ShopifyResource.activate_session(new_session)
                existing_script_tags = shopify.ScriptTag.find()
                if existing_script_tags:
                    for script_tag in existing_script_tags:
                        if script_tag.src != self.shopify_script_tag_url:
                            shopify.ScriptTag.find(script_tag.id).destroy()
                            shopify.ScriptTag.create({
                                "event": "onload",
                                "src": self.shopify_script_tag_url
                            })
                else:
                    shopify.ScriptTag.create({
                        "event": "onload",
                        "src": self.shopify_script_tag_url
                    })
                shop.is_update_script_tag = True
            print("end cron job change_script_tag!")
        except Exception as e:
            print(e)


class InstafeedConfig(models.TransientModel):
    _inherit = 'res.config.settings'
    api_key_instafeed = fields.Char()
    secret_key_instafeed = fields.Char()
    api_version_instafeed = fields.Char()
    ig_app_id = fields.Char()
    # api_key_instagram = fields.Char()
    secret_key_instagram = fields.Char()
    fb_app_id = fields.Char()
    # api_key_facebook = fields.Char()
    secret_key_facebook = fields.Char()
    tiktok_app_id = fields.Char()
    secret_key_tiktok = fields.Char()

    @api.model
    def get_values(self):
        res = super().get_values()
        params = self.env['ir.config_parameter'].sudo()
        res.update(
            api_key_instafeed=str(params.get_param('instafeed.api_key_instafeed')),
            secret_key_instafeed=str(params.get_param('instafeed.secret_key_instafeed')),
            api_version_instafeed=str(params.get_param('instafeed.api_version_instafeed')),
            ig_app_id=str(params.get_param('instafeed.ig_app_id')),
            # api_key_instagram=str(params.get_param('instafeed.api_key_instagram')),
            secret_key_instagram=str(params.get_param('instafeed.secret_key_instagram')),
            fb_app_id=str(params.get_param('instafeed.fb_app_id')),
            # api_key_facebook=str(params.get_param('instafeed.api_key_facebook')),
            secret_key_facebook=str(params.get_param('instafeed.secret_key_facebook')),
            tiktok_app_id=str(params.get_param('instafeed.tiktok_app_id')),
            secret_key_tiktok=str(params.get_param('instafeed.secret_key_tiktok')),

        )
        return res

    def set_values(self):
        super().set_values()
        param = self.env['ir.config_parameter'].sudo()
        field_api_key = self.api_key_instafeed if self.api_key_instafeed else False
        field_secret_key = self.secret_key_instafeed if self.secret_key_instafeed else False
        field_api_version = self.api_version_instafeed if self.api_version_instafeed else False
        field_ig_app_id = self.ig_app_id if self.ig_app_id else False
        # field_api_key_instagram = self.api_key_instagram if self.api_key_instagram else False
        field_secret_key_instagram = self.secret_key_instagram if self.secret_key_instagram else False
        field_fb_app_id = self.fb_app_id if self.fb_app_id else False
        # field_api_key_facebook = self.api_key_facebook if self.api_key_facebook else False
        field_secret_key_facebook = self.secret_key_facebook if self.secret_key_facebook else False
        field_tiktok_app_id = self.tiktok_app_id if self.tiktok_app_id else False
        field_secret_key_tiktok = self.secret_key_tiktok if self.secret_key_tiktok else False

        param.set_param('instafeed.api_key_instafeed', field_api_key)
        param.set_param('instafeed.secret_key_instafeed', field_secret_key)
        param.set_param('instafeed.api_version_instafeed', field_api_version)
        param.set_param('instafeed.ig_app_id', field_ig_app_id)
        # param.set_param('instafeed.api_key_instagram', field_api_key_instagram)
        param.set_param('instafeed.secret_key_instagram', field_secret_key_instagram)
        param.set_param('instafeed.fb_app_id', field_fb_app_id)
        # param.set_param('instafeed.api_key_facebook', field_api_key_facebook)
        param.set_param('instafeed.secret_key_facebook', field_secret_key_facebook)
        param.set_param('instafeed.tiktok_app_id', field_tiktok_app_id)
        param.set_param('instafeed.secret_key_tiktok', field_secret_key_tiktok)
