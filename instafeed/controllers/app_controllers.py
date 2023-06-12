from odoo import http, fields
from odoo.http import request
import requests
import werkzeug
from odoo.modules import get_resource_path
from datetime import datetime
import shopify, base64, json, string, random

scopes = [
    "read_products",
    "read_orders",
    'read_script_tags',
    'write_script_tags',
    "read_draft_orders",
    'write_draft_orders',
    'read_themes',
    'write_themes'
]


class InstafeedController(http.Controller):
    @http.route('/instafeed/install', auth='public')
    def install_instafeed(self, **kwargs):
        try:
            if "shop" in kwargs:
                api_key = request.env['ir.config_parameter'].sudo().get_param('instafeed.api_key_instafeed')
                secret_key = request.env['ir.config_parameter'].sudo().get_param('instafeed.secret_key_instafeed')
                base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
                api_version = request.env['ir.config_parameter'].sudo().get_param('instafeed.api_version_instafeed')

                shopify.Session.setup(api_key=api_key, secret=secret_key)
                print(shopify)
                state = kwargs['hmac']
                callback = request.env['ir.config_parameter'].sudo().get_param(
                    'web.base.url') + '/instafeed/oauth/callback'
                new_session = shopify.Session(kwargs['shop'], api_version)
                auth_url = new_session.create_permission_url(scopes, callback, state)
                return werkzeug.utils.redirect(auth_url)
        except Exception as e:
            print(e)
            return werkzeug.utils.redirect('https://shopify.com/')

    @http.route('/instafeed/oauth/callback', type="http", auth="public", website=True, method=['GET'], csrf=False)
    def instafeed_callback(self, **kwargs):
        try:
            if 'shop' in kwargs:
                api_key = request.env['ir.config_parameter'].sudo().get_param('instafeed.api_key_instafeed')
                secret_key = request.env['ir.config_parameter'].sudo().get_param('instafeed.secret_key_instafeed')
                base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
                api_version = request.env['ir.config_parameter'].sudo().get_param('instafeed.api_version_instafeed')
                shopify.Session.setup(api_key=api_key, secret=secret_key)
                session = shopify.Session(kwargs["shop"], api_version)
                access_token = session.request_token(kwargs)
                shopify.ShopifyResource.activate_session(session)
                shopify_infor = shopify.GraphQL().execute('''
                             {
                                 shop{
                                     id 
                                     name 
                                     email
                                     currencyCode 
                                     url 
                                     billingAddress{
                                         country
                                     }
                                 }
                             }''')
                shopify_data = json.loads(shopify_infor)
                shopify_id = shopify_data["data"]["shop"]["id"].split("/")[-1]
                if access_token:
                    existing_webhooks = shopify.Webhook.find()
                    ngrok_url = request.env['ir.config_parameter'].sudo().get_param('instafeed.ngrok_url')
                    if not ngrok_url:
                        ngrok_url = 'https://66f8-2405-4802-1cdf-bcb0-191e-dfcd-2d7b-9853.ngrok-free.app/'
                    if not existing_webhooks:
                        print("existing_webhooks")

                        webhook_products_create = shopify.Webhook()
                        webhook_products_create.topic = "products/create"
                        webhook_products_create.address = f"{ngrok_url}/webhook/products_create/{shopify_id}"
                        webhook_products_create.format = "json"
                        webhook_products_create.save()
                        print(f"{webhook_products_create.id}: {webhook_products_create.topic}")

                        webhook_products_update = shopify.Webhook()
                        webhook_products_update.topic = "products/update"
                        webhook_products_update.address = f"{ngrok_url}/webhook/products_update/{shopify_id}"
                        webhook_products_update.format = "json"
                        webhook_products_update.save()
                        print(f"{webhook_products_update.id}: {webhook_products_update.topic}")
                    else:
                        print('existing_webhooks:')
                        for webhook in existing_webhooks:
                            print(f"---{webhook.id}: {webhook.topic}")

                    existing_script_tags = shopify.ScriptTag.find()
                    new_script_tag_url = f'{base_url}/instafeed/static/js/extension.js?v={str(datetime.now())}'
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
                    except Exception as e:
                        print(e)
                    password_generate = ''.join(random.choice(string.ascii_letters) for i in range(20))
                    current_user = request.env.user
                    if request.env.user.id == request.env.ref('base.public_user').id:
                        return werkzeug.utils.redirect('/web/login')
                    else:
                        current_shopify = shopify.Shop.current()
                        current_shop = request.env["shopify.store"].sudo().search([("shop_id", "=", shopify_id)],
                                                                                  limit=1)
                        if current_shop:
                            current_shop.status = True
                            if not current_shop.shopify_owner:
                                current_shop.shopify_owner = current_shopify.shop_owner
                                current_shop.sudo().write({
                                    "access_token": access_token,
                                    "name": shopify_data["data"]["shop"]["name"],
                                    "email": shopify_data["data"]["shop"]["email"],
                                    "currency": shopify_data["data"]["shop"]["currencyCode"],
                                    "url": shopify_data["data"]["shop"]["url"],
                                    "country": shopify_data["data"]["shop"]["billingAddress"]["country"]
                                })
                        else:
                            current_shop = request.env["shopify.store"].sudo().create({
                                "shop_id": shopify_id,
                                'access_token': access_token,
                                "name": shopify_data["data"]["shop"]["name"],
                                "email": shopify_data["data"]["shop"]["email"],
                                'status': True,
                                "currency": shopify_data["data"]["shop"]["currencyCode"],
                                "url": shopify_data["data"]["shop"]["url"],
                                "country": shopify_data["data"]["shop"]["billingAddress"]["country"]
                            })
                        if not current_shop.admin:
                            current_shop.admin = current_user.id
                        else:
                            if current_user.id == current_shop.admin.id:
                                return werkzeug.utils.redirect(base_url + '/instafeed')
                            else:
                                return werkzeug.utils.redirect(base_url + '/instafeed/error')
                        if not existing_script_tags:
                            if not new_script_tag:
                                current_shop.is_update_script_tag = False
                            else:
                                current_shop.is_update_script_tag = True
                        else:
                            current_shop.is_update_script_tag = True
                        return werkzeug.utils.redirect(base_url + '/instafeed')
        except Exception as e:
            print(e)
        return werkzeug.utils.redirect('https://shopify.com/')

    @http.route('/instafeed/get/data', type='http', auth='user', csrf=False)
    def get_data(self, **kwargs):
        try:
            current_user = request.env.user
            store_info = request.env['shopify.store'].sudo().search([("admin", '=', current_user.id)], limit=1)
            media_sources = request.env['media.source'].sudo().search([('admin', '=', current_user.id)])
            facebook_accounts = request.env['social.account'].sudo().search(
                [('admin', '=', current_user.id), ('type', '=', 'facebook')])
            instagram_accounts = request.env['social.account'].sudo().search(
                [('admin', '=', current_user.id), ('type', '=', 'instagram')])
            tiktok_accounts = request.env['social.account'].sudo().search(
                [('admin', '=', current_user.id), ('type', '=', 'tiktok')])
            widget_datas = request.env['widget.data'].sudo().search([('admin', '=', current_user.id)])
            list_media_sources = []
            for media_source in media_sources:
                list = []
                for post in media_source.selected_private_posts:
                    list_tags = []
                    for hotspot in post.hotspot:
                        list_tags.append(int(hotspot.product_id))
                    list.append({
                        'post_id': post.post_id,
                        'media_url': post.media_url,
                        'type': post.type,
                        'caption': post.caption,
                        'insta_profile_link': post.insta_profile_link,
                        'thumbnail_url': post.thumbnail_url,
                        'like_count': post.like_count,
                        'comments_count': post.comments_count,
                        'link_to_post': post.link_to_post,
                        'instagram_business_account_username': media_source.social_account.instagram_business_account_username,
                        'instagram_business_account_followers_count': media_source.social_account.instagram_business_account_followers_count,
                        'facebook_id': media_source.social_account.id if media_source.social_account.type == 'facebook' else False,
                        'instagram_id': media_source.social_account.id if media_source.social_account.type == 'instagram' else False,
                        'instagram_username': media_source.social_account.username,
                        'list_tags': list_tags,
                        'tiktok': post.tiktok
                    })
                list_media_sources.append({
                    'id': media_source.id,
                    'name': media_source.name,
                    'social_account': {
                        'username': media_source.social_account.username,
                        'user_id': media_source.social_account.user_id
                    },

                    'posts': list
                })
            list_facebook_accounts = []
            for facebook_account in facebook_accounts:
                list = []
                for post in facebook_account.posts:
                    list.append({
                        'post_id': post.post_id,
                        'media_url': post.media_url,
                        'type': post.type,
                        'caption': post.caption,
                        'insta_profile_link': post.insta_profile_link,
                        'thumbnail_url': post.thumbnail_url,
                        'like_count': post.like_count,
                        'comments_count': post.comments_count,
                        'link_to_post': post.link_to_post
                    })
                vals = {
                    'user_id': facebook_account.user_id,
                    'url_image': facebook_account.url_image,
                    'username': facebook_account.username,
                    'status': facebook_account.status,
                    'instagram_business_account_id': facebook_account.instagram_business_account_id,
                    'instagram_business_account_username': facebook_account.instagram_business_account_username,
                    'instagram_business_account_followers_count': facebook_account.instagram_business_account_followers_count,
                    'posts': list
                }
                list_facebook_accounts.append(vals)
            list_instagram_accounts = []
            for instagram_account in instagram_accounts:
                list = []
                for post in instagram_account.posts:
                    list.append({
                        'post_id': post.post_id,
                        'media_url': post.media_url,
                        'type': post.type,
                        'caption': post.caption,
                        'insta_profile_link': post.insta_profile_link,
                        'thumbnail_url': post.thumbnail_url,
                        'link_to_post': post.link_to_post
                    })
                vals = {
                    'user_id': instagram_account.user_id,
                    'username': instagram_account.username,
                    'posts': list
                }
                list_instagram_accounts.append(vals)
            list_tiktok_accounts = []
            for tiktok_account in tiktok_accounts:
                list = []
                for post in tiktok_account.posts:
                    list.append({
                        'post_id': post.post_id,
                        'media_url': post.media_url,
                        'type': post.type,
                        'caption': post.caption,
                        'insta_profile_link': post.insta_profile_link,
                        'thumbnail_url': post.thumbnail_url,
                        'like_count': post.like_count,
                        'comments_count': post.comments_count,
                        'link_to_post': post.link_to_post,
                        'tiktok': post.tiktok
                    })
                vals = {
                    'user_id': tiktok_account.user_id,
                    'url_image': tiktok_account.url_image,
                    'username': tiktok_account.username,
                    'status': tiktok_account.status,
                    'posts': list
                }
                list_tiktok_accounts.append(vals)
            list_widgets = []
            for widget in widget_datas:
                analytics = request.env['analytics'].sudo().search([('feed_id', '=', widget.id)])
                analytic_days = []
                for analytic in analytics:
                    analytic_days.append({
                        'day': analytic.date.strftime('%Y-%m-%d'),
                        'analytics': json.loads(analytic.json_analytics)
                    })
                list_media_sources_id = []
                widget_config = request.env['widget.config'].sudo().search([('widget', '=', widget.id)], limit=1)
                for media_source in widget.media_sources:
                    list_media_sources_id.append(media_source.id)
                list_widgets.append({
                    'widget_name': widget.name,
                    'feed_id': widget.id,
                    'feed_title': widget_config.feed_title,
                    'post_spacing': widget_config.post_spacing,
                    'on_post_click': widget_config.on_post_click,
                    'layout': widget_config.layout,
                    'configuration': widget_config.configuration,
                    'per_slide': widget_config.per_slide,
                    'number_of_posts': widget_config.number_of_posts,
                    'number_of_rows': widget_config.number_of_rows,
                    'number_of_columns': widget_config.number_of_columns,
                    'show_likes': widget_config.show_likes,
                    'show_followers': widget_config.show_followers,
                    'media_sources_id': list_media_sources_id,
                    'analytic_days': analytic_days
                })
            social_accounts = {
                'facebook_accounts': list_facebook_accounts,
                'instagram_accounts': list_instagram_accounts,
                'tiktok_accounts': list_tiktok_accounts
            }
            products = []
            try:
                products = self.get_shopify_product()
            except Exception as e:
                print(e)
            data = {
                'media_sources': list_media_sources,
                'social_accounts': social_accounts,
                'username': store_info.shopify_owner,
                'products': products,
                'widgets': list_widgets,
                'shop_url': store_info.url
            }
            return json.dumps(data)
        except Exception as e:
            print(e)
        return json.dumps({'error': 'error'})

    @http.route('/instafeed/create/media_source', type='json', auth='user', csrf=False)
    def create_media_source(self, **kwargs):
        try:
            res = json.loads(request.httprequest.data)
            print(res)
            current_user = request.env.user
            facebook_account = request.env['social.account'].sudo().search(
                [('admin', '=', current_user.id), ('user_id', '=', res['user_id']), ('type', '=', 'facebook')],
                limit=1)
            instagram_account = request.env['social.account'].sudo().search(
                [('type', '=', 'instagram'), ('admin', '=', current_user.id), ('user_id', '=', res['user_id'])],
                limit=1)
            tiktok_account = request.env['social.account'].sudo().search(
                [('type', '=', 'tiktok'), ('admin', '=', current_user.id), ('user_id', '=', res['user_id'])],
                limit=1)
            media_source = request.env['media.source'].sudo().create(
                {'admin': current_user.id,
                 'social_account': instagram_account.id if instagram_account else facebook_account.id if facebook_account else tiktok_account.id if tiktok_account else None,
                 'name': res['name']})
            return {'id': media_source.id,
                    'name': media_source.name,
                    'social_account': {
                        'username': media_source.social_account.username,
                        'user_id': media_source.social_account.user_id,
                    },
                    'posts': []
                    }
        except Exception as e:
            print(e)
            return json.dumps({'error': 'error'})

    @http.route('/instafeed/create/widget', type='json', auth='user', csrf=False)
    def create_widget(self, **kwargs):
        res = json.loads(request.httprequest.data)
        print(res)
        current_user = request.env.user
        widget = request.env['widget.data'].sudo().create({'admin': current_user.id,
                                                           'name': res['name']})
        widget_config = request.env['widget.config'].sudo().create({'admin': current_user.id,
                                                                    'widget': widget.id})
        widget.write({'widget_config': widget_config.id})
        media_sources = request.env['media.source'].sudo().search(
            [('admin', '=', current_user.id), ('id', 'in', res['list_media_sources_id'])])
        for media_source in media_sources:
            print(media_source)
            widget.write({'media_sources': [(4, media_source.id)]})
        print(widget)
        print(widget.media_sources)
        return {'widget_name': widget.name,
                'feed_id': widget.id,
                'feed_title': widget_config.feed_title,
                'post_spacing': widget_config.post_spacing,
                'on_post_click': widget_config.on_post_click,
                'layout': widget_config.layout,
                'configuration': widget_config.configuration,
                'per_slide': widget_config.per_slide,
                'number_of_posts': widget_config.number_of_posts,
                'number_of_rows': widget_config.number_of_rows,
                'number_of_columns': widget_config.number_of_columns,
                'show_likes': widget_config.show_likes,
                'show_followers': widget_config.show_followers,
                'media_sources_id': res['list_media_sources_id']}

    @http.route('/instafeed/save/media_source', type='json', auth='user', csrf=False)
    def save_media_source(self, **kwargs):
        try:
            current_user = request.env.user
            print('haha')
            res = json.loads(request.httprequest.data)
            print(res)
            facebook_account = request.env['social.account'].sudo().search(
                [('admin', '=', current_user.id), ('user_id', '=', res['user_id']), ('type', '=', 'facebook')],
                limit=1)
            instagram_account = request.env['social.account'].sudo().search(
                [('admin', '=', current_user.id), ('user_id', '=', res['user_id']), ('type', '=', 'instagram')],
                limit=1)
            tiktok_account = request.env['social.account'].sudo().search(
                [('admin', '=', current_user.id), ('user_id', '=', res['user_id']), ('type', '=', 'tiktok')],
                limit=1)
            media_source = request.env['media.source'].sudo().search(
                [('admin', '=', current_user.id), ('id', '=', res['media_source_id'])], limit=1)
            for post in media_source.selected_private_posts:
                if str(post.post_id) not in res['list_selected_post_id']:
                    media_source.write({'selected_private_posts': [(3, post.id)]})
            for post_id in res['list_selected_post_id']:
                post = request.env['post.private'].sudo().search(
                    [('post_id', '=', post_id), ('admin', '=', current_user.id),
                     ('social_account', '=', facebook_account.id)])
                if not post:
                    post = request.env['post.private'].sudo().search(
                        [('post_id', '=', post_id), ('admin', '=', current_user.id),
                         ('social_account', '=', instagram_account.id)])
                    if not post:
                        post = request.env['post.private'].sudo().search(
                            [('post_id', '=', post_id), ('admin', '=', current_user.id),
                             ('social_account', '=', tiktok_account.id)])
                media_source.write({'selected_private_posts': [(4, post.id)]})
            list = []
            for post in media_source.selected_private_posts:
                list.append({
                    'facebook_id': media_source.social_account.id if media_source.social_account.type == 'facebook' else False,
                    'instagram_id': media_source.social_account.id if media_source.social_account.type == 'instagram' else False,
                    'post_id': post.post_id,
                    'media_url': post.media_url,
                    'type': post.type,
                    'caption': post.caption,
                    'insta_profile_link': post.insta_profile_link,
                    'thumbnail_url': post.thumbnail_url,
                    'like_count': post.like_count,
                    'comments_count': post.comments_count,
                    # 'create_date': json.dumps(post.create_date),
                    'link_to_post': post.link_to_post,
                    'instagram_business_account_username': media_source.social_account.instagram_business_account_username,
                    'instagram_business_account_followers_count': media_source.social_account.instagram_business_account_followers_count,
                })
            return {'id': media_source.id,
                    'name': media_source.name,
                    'social_account': {
                        'username': media_source.social_account.username,
                        'user_id': media_source.social_account.user_id
                    },
                    'posts': list
                    }
        except Exception as e:
            print(e)
            return json.dumps({'error': 'error'})

    @http.route('/instafeed/save/feed', type='json', auth='user', csrf=False)
    def save_feed(self, **kwargs):
        # try:
        print('haha')
        current_user = request.env.user
        res = json.loads(request.httprequest.data)
        widget = request.env['widget.data'].sudo().search(
            [('id', '=', res['feed']['widget']), ('admin', '=', current_user.id)], limit=1)
        widget_config = request.env['widget.config'].sudo().search(
            [('widget', '=', widget.id), ('admin', '=', current_user.id)], limit=1)
        widget_config.write(res['feed'])
        for post in res['posts']:
            # print(json.dumps(post['list_tags']))
            post_exist = request.env['post.private'].sudo().search(
                [('post_id', '=', post['post_id']), ('admin', '=', current_user.id),
                 ('social_account', '=', int(post['facebook_id']))],
                limit=1)
            a = request.env['post.private'].sudo().search(
                [('post_id', '=', post['post_id']), ('admin', '=', current_user.id),
                 ('social_account', '=', int(post['instagram_id']))],
                limit=1)
            if not post_exist:
                post_exist = request.env['post.private'].sudo().search(
                    [('post_id', '=', post['post_id']), ('admin', '=', current_user.id),
                     ('social_account', '=', int(post['instagram_id']))],
                    limit=1)
            if 'list_tags' in post:
                print(post['list_tags'])
                for product_id in post['list_tags']:
                    print(str(product_id))
                    hotspot = request.env['hotspot.private'].sudo().search(
                        [('product_id', '=', str(product_id)), ('admin', '=', current_user.id)])
                    if hotspot:
                        hotspot.write({'post_id': post_exist.id})
                    else:
                        request.env['hotspot.private'].sudo().create({
                            'product_id': str(product_id),
                            'admin': current_user.id,
                            'post_id': post_exist.id
                        })
        return {'status': 'success'}

    # except Exception as e:
    #     print(e)
    #     return json.dumps({'error': 'error'})

    @http.route('/instafeed/delete/media_source', type='json', auth='user', csrf=False)
    def delete_media_source(self, **kwargs):
        try:
            res = json.loads(request.httprequest.data)
            print(res)
            media_source = request.env['media.source'].sudo().search([('id', '=', res['media_source_id'])], limit=1)
            media_source.unlink()
            return {'status': 'success'}
        except Exception as e:
            print(e)
            return json.dumps({'error': 'error'})

    @http.route('/instafeed/delete/widget', type='json', auth='user', csrf=False)
    def delete_widget(self, **kwargs):
        try:
            res = json.loads(request.httprequest.data)
            print(res)
            widget = request.env['widget.data'].sudo().search([('id', '=', res['widget_id'])], limit=1)
            widget_config = request.env['widget.config'].sudo().search([('widget', '=', widget.id)], limit=1)
            widget.unlink()
            return {'status': 'success'}
        except Exception as e:
            print(e)
            return json.dumps({'error': 'error'})

    @http.route('/instafeed/change/widget_name', type='json', auth='user', csrf=False)
    def change_widget_name(self, **kwargs):
        try:
            current_user = request.env.user
            res = json.loads(request.httprequest.data)
            print(res)
            widget = request.env['widget.data'].sudo().search(
                [('admin', '=', current_user.id), ('id', '=', res['widget_id'])], limit=1)
            widget.name = res['widget_name']
            return {'status': 'success'}
        except Exception as e:
            print(e)
            return json.dumps({'error': 'error'})

    @http.route('/instafeed/show/feed', type='json', auth='public', csrf=False)
    def show_feed(self, **kwargs):
        res = json.loads(request.httprequest.data)
        print(res)
        shop_url = res['shop_url']
        shop = request.env['shopify.store'].sudo().search([('url', '=', f"https://{shop_url}")], limit=1)
        widget = request.env['widget.data'].sudo().search(
            [('admin', '=', shop.admin.id), ('id', '=', int(res['feed_id']))], limit=1)
        widget_config = request.env['widget.config'].sudo().search([('widget', '=', widget.id)], limit=1)
        list = []
        products = shop.get_product()
        for media_source in widget.media_sources:
            for post in media_source.selected_private_posts:
                list_tags = []
                for hotspot in post.hotspot:
                    list_tags.append(hotspot.product_id)
                list.append({
                    'post_id': post.post_id,
                    'media_url': post.media_url,
                    'type': post.type,
                    'caption': post.caption,
                    'insta_profile_link': post.insta_profile_link,
                    'thumbnail_url': post.thumbnail_url,
                    'like_count': post.like_count,
                    'comments_count': post.comments_count,
                    'link_to_post': post.link_to_post,
                    'instagram_business_account_username': media_source.social_account.instagram_business_account_username,
                    'instagram_business_account_followers_count': media_source.social_account.instagram_business_account_followers_count,
                    'instagram_username': media_source.social_account.username,
                    'list_tags': list_tags
                })
        return {
            'products': products,
            'feed_id': widget.id,
            'feed_title': widget_config.feed_title,
            'post_spacing': widget_config.post_spacing,
            'on_post_click': widget_config.on_post_click,
            'layout': widget_config.layout,
            'configuration': widget_config.configuration,
            'per_slide': widget_config.per_slide,
            'number_of_posts': widget_config.number_of_posts,
            'number_of_rows': widget_config.number_of_rows,
            'number_of_columns': widget_config.number_of_columns,
            'show_likes': widget_config.show_likes,
            'show_followers': widget_config.show_followers,
            'posts': list
        }

    @http.route('/instafeed/analytics', type='json', auth='public', csrf=False)
    def analytics_post(self, **kwargs):
        res = json.loads(request.httprequest.data)
        today = datetime.today().date()
        print(today)
        print(res)
        analytics = request.env['analytics'].sudo().search([('feed_id', '=', int(res['feed_id']))])
        print(analytics)
        check = 0
        if analytics:
            for analytic in analytics:
                if analytic.date == today:
                    if analytic.json_analytics:
                        vals = json.loads(analytic.json_analytics)
                    else:
                        vals = {
                            'posts': 0,
                            'feeds': 0,
                            'products': 0,
                        }
                    if 'is_clicked' in res:
                        if not res['is_clicked']:
                            vals['feeds'] += 1
                    if 'post_id' in res:
                        vals['posts'] += 1
                    if 'product_id' in res:
                        vals['products'] += 1
                    analytic.json_analytics = json.dumps(vals)
                    print(analytic.json_analytics)
                    check = 1
                    break
        if not check:
            vals = {
                'posts': 0,
                'feeds': 0,
                'products': 0,
            }
            if 'is_clicked' in res:
                if not res['is_clicked']:
                    vals['feeds'] += 1
            if 'post_id' in res:
                vals['posts'] += 1
            if 'product_id' in res:
                vals['products'] += 1
            analytic = request.env['analytics'].sudo().create({'feed_id': int(res['feed_id']),
                                                               'date': today,
                                                               'json_analytics': json.dumps(vals)})

    def get_shopify_product(self, **kwargs):
        current_user = request.env.user
        store_info = request.env['shopify.store'].sudo().search([("admin", '=', current_user.id)], limit=1)
        if store_info:
            return store_info.get_product()
        else:
            return {}
