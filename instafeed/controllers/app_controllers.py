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
    'write_draft_orders'
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

                    current_company = request.env['res.company'].sudo().search([('name', '=', kwargs['shop'])], limit=1)
                    current_user = request.env['res.users'].sudo().search([('login', '=', kwargs['shop'])], limit=1)
                    password_generate = ''.join(random.choice(string.ascii_letters) for i in range(20))

                    if not current_company:
                        current_company = request.env['res.company'].sudo().create({
                            'logo': False,
                            'currency_id': 2,
                            'sequence': 10,
                            'name': kwargs['shop'],
                            'street': False,
                            'street2': False,
                            'city': False,
                            'state_id': False,
                            'zip': False,
                            'country_id': False,
                            'phone': False,
                            'email': False,
                            'website': False,
                            'vat': False,
                            'company_registry': False,
                            'parent_id': False
                        })

                    if not current_user:
                        current_user = request.env['res.users'].sudo().create({
                            'company_ids': [[6, False, [current_company.id]]],
                            'company_id': current_company.id,
                            'active': True,
                            'lang': 'en_US',
                            'tz': 'Europe/Brussels',
                            '__last_update': False,
                            'name': kwargs['shop'],
                            'email': shopify_data["data"]["shop"]["email"],
                            'login': kwargs['shop'],
                            'password': password_generate,
                            'action_id': False,
                        })

                    current_shopify = shopify.Shop.current()
                    current_shop = request.env["shopify.store"].sudo().search([("shop_id", "=", shopify_id)], limit=1)
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
                    print(current_user.password)
                    if not current_shop.admin:
                        current_shop.admin = current_user.id
                    if not current_shop.password:
                        current_shop.password = password_generate
                    if not existing_script_tags:
                        if not new_script_tag:
                            current_shop.is_update_script_tag = False
                        else:
                            current_shop.is_update_script_tag = True
                    else:
                        current_shop.is_update_script_tag = True
                    db = http.request.env.cr.dbname
                    request.env.cr.commit()
                    request.session.authenticate(db, kwargs['shop'], current_shop.password)
                    return werkzeug.utils.redirect(base_url + '/instafeed')
        except Exception as e:
            print(e)
        return werkzeug.utils.redirect('https://shopify.com/')

    @http.route('/instafeed/get/data', type='http', auth='user', csrf=False)
    def get_data(self, **kwargs):
        try:
            curren_user = request.env.user
            media_sources = request.env['media.source'].sudo().search([('admin', '=', curren_user.id)])
            facebook_accounts = request.env['facebook.account'].sudo().search([('admin', '=', curren_user.id)])
            widget_datas = request.env['widget.data'].sudo().search([('admin', '=', curren_user.id)])
            list_media_sources = []
            for media_source in media_sources:
                list = []
                for post in media_source.selected_private_posts_advance:
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
                        # 'create_date': json.dumps(post.create_date),
                        'link_to_post': post.link_to_post,
                        'instagram_business_account_username': media_source.facebook_account.instagram_business_account_username,
                        'instagram_business_account_followers_count': media_source.facebook_account.instagram_business_account_followers_count,
                        # 'list_tag': json.loads(post.list_tags),
                        'facebook_id': media_source.facebook_account.id,
                        'list_tags': list_tags
                    })
                list_media_sources.append({
                    'id': media_source.id,
                    'name': media_source.name,
                    'social_account': {'username': media_source.facebook_account.username,
                                       'user_id': media_source.facebook_account.user_id,
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
                        # 'create_date': json.dumps(post.create_date),
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
            list_widgets = []
            for widget in widget_datas:
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
                    'media_sources_id': list_media_sources_id
                })
            social_accounts = {
                'facebook_accounts': list_facebook_accounts
            }
            products = self.get_shopify_product()
            print(products)
            data = {
                'media_sources': list_media_sources,
                'social_accounts': social_accounts,
                'username': curren_user.login,
                'products': products,
                'widgets': list_widgets
            }
            return json.dumps(data)
        except Exception as e:
            print(e)
        return json.dumps({'error': 'error'})

    # @http.route('/instafeed/create/widget', type='http', auth='user', csrf=False)
    # def create_feed(self, **kwargs):
    #     current_user = request.env.user
    #     feed = request.env['widget.data'].sudo().create({'admin': current_user.id})
    #     return json.dumps({'feed_id': feed.id})

    @http.route('/instafeed/create/media_source', type='json', auth='user', csrf=False)
    def create_media_source(self, **kwargs):
        try:
            res = json.loads(request.httprequest.data)
            print(res)
            current_user = request.env.user
            facebook_account = request.env['facebook.account'].sudo().search([('user_id', '=', res['user_id'])],
                                                                             limit=1)
            media_source = request.env['media.source'].sudo().create(
                {'admin': current_user.id, 'facebook_account': facebook_account.id,
                 'name': res['name']})
            return {'id': media_source.id,
                    'name': media_source.name,
                    'social_account': {
                        'username': media_source.facebook_account.username,
                        'user_id': media_source.facebook_account.user_id
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
        media_sources = request.env['media.source'].sudo().search([('id', 'in', res['list_media_sources_id'])])
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
            print('haha')
            res = json.loads(request.httprequest.data)
            print(res)
            facebook_account = request.env['facebook.account'].sudo().search([('user_id', '=', res['user_id'])],
                                                                             limit=1)
            media_source = request.env['media.source'].sudo().search([('id', '=', res['media_source_id'])], limit=1)
            for post in media_source.selected_private_posts_advance:
                if str(post.post_id) not in res['list_selected_post_id']:
                    media_source.write({'selected_private_posts_advance': [(3, post.id)]})
            for post_id in res['list_selected_post_id']:
                post = request.env['post.private.advance'].sudo().search(
                    [('post_id', '=', post_id), ('facebook_user', '=', facebook_account.id)])
                media_source.write({'selected_private_posts_advance': [(4, post.id)]})
            list = []
            for post in media_source.selected_private_posts_advance:
                list.append({
                    'post_id': post.post_id,
                    'media_url': post.media_url,
                    'type': post.type,
                    'caption': post.caption,
                    'insta_profile_link': post.insta_profile_link,
                    'thumbnail_url': post.thumbnail_url,
                    'like_count': post.like_count,
                    'comments_count': post.comments_count,
                    # 'create_date': json.dumps(post.create_date),
                    'link_to_post': post.link_to_post
                })
            return {'id': media_source.id,
                    'name': media_source.name,
                    'social_account': {
                        'username': media_source.facebook_account.username,
                        'user_id': media_source.facebook_account.user_id
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
            post_exist = request.env['post.private.advance'].sudo().search(
                [('post_id', '=', post['post_id']), ('facebook_user', '=', int(post['facebook_id']))],
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
                    print(hotspot)
                # for product_id in post['list_tags']:
                #     print(post['list_tags'])
                #     hotspot = request.env['hotspot.private'].sudo().search(['product_id', '=', str(product_id), ('admin', '=', current_user.id)])
                #     if hotspot:
                #         hotspot.write({'post_id': post_exist.id})
                #     else:
                #         request.env['hotspot.private'].sudo().create({
                #             'product_id': str(product_id),
                #             'admin': current_user.id,
                #             'post_id': post_exist.id
                #         })
                #     print(str(product_id))
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

    # @http.route('/instafeed/delete', type='json', auth='user', csrf=False)
    # def delete_feed(self, **kwargs):
    #     res = json.loads(request.httprequest.data)
    #     feed = request.env['instafeed'].sudo().search([('id', '=', int(res['feed_id']))])
    #     facebook = request.env['facebook'].sudo().search([('feed_id', '=', feed.id)])
    #     for post in facebook.posts:
    #         post.unlink()
    #     facebook.unlink()
    #     feed.unlink()
    #     return ({'status': 'success'})
    #
    # @http.route('/instafeed/save', type='json', auth="user")
    # def save_feed(self, **kwargs):
    #     if request.httprequest.data:
    #         res = json.loads(request.httprequest.data)
    #         feed = res['feed']
    #         posts = res['posts']
    #         feed_id = res['feed_id']
    #         shop_url = request.session['shop_url']
    #         shop = request.env['shop'].sudo().search([('shop_url', '=', shop_url)], limit=1)
    #         instafeed_user = request.env['instafeed'].sudo().search([('id', '=', int(feed_id))], limit=1)
    #         facebook_user = request.env['facebook'].sudo().search([('feed_id', '=', instafeed_user.id)], limit=1)
    #         for post in posts:
    #             post_exist = request.env['instagram.post'].sudo().search(
    #                 [('facebook_id', '=', facebook_user.id), ('post_id', '=', post['id'])], limit=1)
    #             if post_exist:
    #                 for product in post_exist.products:
    #                     if product.product_id not in post['list_tags']:
    #                         post_exist.write({'products': [(3, request.env['shopify.product'].sudo().search(
    #                             [('product_id', '=', product.product_id), ('store_id', '=', shop.id)]).id)]})
    #                 for product_id in post['list_tags']:
    #                     product_exist = request.env['shopify.product'].sudo().search(
    #                         [('product_id', '=', product_id), ('store_id', '=', shop.id)])
    #                     if product_exist:
    #                         post_exist.write({'products': [(4, product_exist.id)]})
    #                     else:
    #                         product_exist = request.env['shopify.product'].sudo().create({
    #                             'product_id': product_id,
    #                             'store_id': shop.id,
    #                         })
    #                         post_exist.write({'products': [(4, product_exist.id)]})
    #             else:
    #                 post_exist = request.env['instagram.post'].sudo().create({
    #                     'facebook_id': facebook_user.id,
    #                     'post_id': post['id']
    #                 })
    #                 for product in post_exist.products:
    #                     if product.product_id not in post['list_tags']:
    #                         post_exist.write({'products': [(3, request.env['shopify.product'].sudo().search(
    #                             [('product_id', '=', product.product_id), ('store_id', '=', shop.id)]).id)]})
    #                 for product_id in post['list_tags']:
    #                     product_exist = request.env['shopify.product'].sudo().search(
    #                         [('product_id', '=', product_id), ('store_id', '=', shop.id)])
    #                     print(post_exist.id)
    #                     if product_exist:
    #                         post_exist.write({'products': [(4, product_exist.id)]})
    #                     else:
    #                         product_exist = request.env['shopify.product'].sudo().create({
    #                             'product_id': product_id,
    #                             'store_id': shop.id,
    #                         })
    #                         post_exist.write({'products': [(4, product_exist.id)]})
    #         if instafeed_user:
    #             instafeed_user.write(feed)
    #         else:
    #             feed['store_id'] = shop.id
    #             request.env['instafeed'].sudo().create(feed)
    #     else:
    #         return False
    #
    # @http.route('/instafeed/get/data', type='json', auth='user', csrf=False)
    # def get_user_info(self, **kwargs):
    #     data = json.loads(request.httprequest.data)
    #     feed_id = data['feed_id']
    #     shop_url = request.session['shop_url']
    #     shop = request.env['shop'].sudo().search([('shop_url', '=', shop_url)], limit=1)
    #     instafeed_user = request.env['instafeed'].sudo().search([('id', '=', int(feed_id))], limit=1)
    #     enpoint = 'https://graph.instagram.com/me?fields=id,username&access_token=' + instafeed_user.long_live_access_token
    #     analytics = request.env['analytics'].sudo().search([('feed_id', '=', int(feed_id))])
    #     analytic_days = []
    #     for analytic in analytics:
    #         analytic_days.append({
    #             'day': analytic.date.strftime('%Y-%m-%d'),
    #             'analytics': json.loads(analytic.json_analytics)
    #         })
    #     res = requests.get(enpoint)
    #     if res.ok:
    #         user = res.json()
    #         instafeed_user.write({'username': user['username']})
    #         media = self.get_media(instafeed_user)
    #         return ({'user': user,
    #                  'user_id': instafeed_user.user_id,
    #                  'media': media,
    #                  'feed_title': instafeed_user.feed_title,
    #                  'post_spacing': instafeed_user.post_spacing,
    #                  'on_post_click': instafeed_user.on_post_click,
    #                  'layout': instafeed_user.layout,
    #                  'configuration': instafeed_user.configuration,
    #                  'per_slide': instafeed_user.per_slide,
    #                  'number_of_posts': instafeed_user.number_of_posts,
    #                  'number_of_rows': instafeed_user.number_of_rows,
    #                  'number_of_columns': instafeed_user.number_of_columns,
    #                  'show_likes': instafeed_user.show_likes,
    #                  'show_followers': instafeed_user.show_followers,
    #                  'feed_id': instafeed_user.id,
    #                  'analytic_days': analytic_days
    #                  })
    #     else:
    #
    #         return False
    #
    # def get_media(self, instafeed_user):
    #     enpoint = 'https://graph.instagram.com/me/media?fields=id,caption,media_type,media_url,thumbnail_url,username,timestamp&access_token=' + instafeed_user.long_live_access_token
    #     res = requests.get(enpoint)
    #     if res.ok:
    #         return res.json()
    #     else:
    #         return False
    #
    # @http.route('/instafeed/get/fb-data', type='json', auth='user', csrf=False)
    # def get_fb_data(self, **kwargs):
    #     shop_url = request.session['shop_url']
    #     data = json.loads(request.httprequest.data)
    #     feed_id = data['feed_id']
    #     shop_url = request.session['shop_url']
    #     shop = request.env['shop'].sudo().search([('shop_url', '=', shop_url)], limit=1)
    #     instafeed_user = request.env['instafeed'].sudo().search([('id', '=', int(feed_id))], limit=1)
    #     facebook_user = request.env['facebook'].sudo().search([('feed_id', '=', instafeed_user.id)], limit=1)
    #     enpoint = 'https://graph.facebook.com/v12.0/me?fields=id,name,accounts&access_token=' + facebook_user.access_token
    #     res = requests.get(enpoint)
    #     if res.ok:
    #         user = res.json()
    #         insta_business_id = self.get_insta_business(user['accounts']['data'][0]['id'], facebook_user)
    #         instagram_info = self.get_info(insta_business_id, facebook_user)
    #         vals = {'fb_username': user['name'],
    #                 'page_id': user['accounts']['data'][0]['id'],
    #                 'instagram_business_account_id': insta_business_id,
    #                 'followers_count': instagram_info['followers_count'],
    #                 }
    #         for post in instagram_info['media']['data']:
    #             post_exist = request.env['instagram.post'].sudo().search(
    #                 [('post_id', '=', post['id']), ('facebook_id', '=', facebook_user.id)], limit=1)
    #             if post_exist:
    #                 post_exist.write({'facebook_id': facebook_user.id,
    #                                   'post_id': post['id']})
    #                 list = []
    #                 for product in post_exist.products:
    #                     list.append(product.product_id)
    #                     post['list_tags'] = list
    #             else:
    #                 post_exist = request.env['instagram.post'].sudo().create({
    #                     'facebook_id': facebook_user.id,
    #                     'post_id': post['id']
    #                 })
    #         facebook_user.write(vals)
    #         vals['media'] = instagram_info['media']
    #         return vals
    #
    # def get_insta_business(self, page_id, facebook_user):
    #     enpoint = 'https://graph.facebook.com/v12.0/' + page_id + '?fields=instagram_business_account&access_token=' + facebook_user.access_token
    #     res = requests.get(enpoint)
    #     if res.ok:
    #         account = res.json()
    #     facebook_user.write({'instagram_business_account_id': account['instagram_business_account']['id']})
    #     return res.json()['instagram_business_account']['id']
    #
    # def get_info(self, insta_business_id, facebook_user):
    #     enpoint = 'https://graph.facebook.com/v12.0/' + insta_business_id + '?fields=name,username,followers_count,media{id,caption,media_type,media_url,thumbnail_url,username,permalink,timestamp,comments_count,comments{from,text},like_count}&access_token=' + facebook_user.access_token
    #     res = requests.get(enpoint)
    #     if res.ok:
    #         account = res.json()
    #     return res.json()
    #
    # @http.route('/instafeed/show/feed', type='json', auth='public', csrf=False)
    # def show_feed(self, **kwargs):
    #     res = json.loads(request.httprequest.data)
    #     shop_url = res['shop_url']
    #     shop = request.env['shop'].sudo().search([('shop_url', '=', shop_url)], limit=1)
    #     instafeed_user = request.env['instafeed'].sudo().search([('id', '=', int(res['feed_id']))], limit=1)
    #     if instafeed_user:
    #         facebook_user = request.env['facebook'].sudo().search([('feed_id', '=', instafeed_user.id)])
    #         enpoint = 'https://graph.instagram.com/me?fields=id,username&access_token=' + instafeed_user.long_live_access_token
    #         res = requests.get(enpoint)
    #         products = json.loads(self.sync_product(shop_url))
    #         print(products)
    #         vals = []
    #         for product in products['products']:
    #             vals.append({
    #                 'product_id': product['id'],
    #                 'name': product['title'],
    #                 'handle': product['handle'],
    #                 'image_url': product['image']['src']
    #             })
    #         if res.ok:
    #             user = res.json()
    #             instafeed_user.write({'username': user['username']})
    #             business_info = self.get_info(facebook_user.instagram_business_account_id, facebook_user)
    #             for post in business_info['media']['data']:
    #                 post_exist = request.env['instagram.post'].sudo().search(
    #                     [('post_id', '=', post['id']), ('facebook_id', '=', facebook_user.id)], limit=1)
    #                 if post_exist:
    #                     post_exist.write({'facebook_id': facebook_user.id,
    #                                       'post_id': post['id']})
    #                     list = []
    #                     for product in post_exist.products:
    #                         list.append(product.product_id)
    #                         post['list_tags'] = list
    #                 else:
    #                     post_exist = request.env['instagram.post'].sudo().create({
    #                         'facebook_id': facebook_user.id,
    #                         'post_id': post['id']
    #                     })
    #             return {'user': user,
    #                     'user_id': instafeed_user.user_id,
    #                     'media': business_info['media'],
    #                     'feed_title': instafeed_user.feed_title,
    #                     'post_spacing': instafeed_user.post_spacing,
    #                     'on_post_click': instafeed_user.on_post_click,
    #                     'layout': instafeed_user.layout,
    #                     'configuration': instafeed_user.configuration,
    #                     'per_slide': instafeed_user.per_slide,
    #                     'number_of_posts': instafeed_user.number_of_posts,
    #                     'number_of_rows': instafeed_user.number_of_rows,
    #                     'number_of_columns': instafeed_user.number_of_columns,
    #                     'show_likes': instafeed_user.show_likes,
    #                     'show_followers': instafeed_user.show_followers,
    #                     'followers_count': business_info['followers_count'],
    #                     'products': vals,
    #                     'feed_id': instafeed_user.id
    #                     }
    #         else:
    #             return False
    #     else:
    #         return False

    # @http.route('/instafeed/analytics', type='json', auth='public', csrf=False)
    # def analytics_post(self, **kwargs):
    #     res = json.loads(request.httprequest.data)
    #     today = datetime.today().date()
    #     print(today)
    #     print(res)
    #     analytics = request.env['analytics'].sudo().search([('feed_id', '=', int(res['feed_id']))])
    #     print(analytics)
    #     check = 0
    #     if analytics:
    #         for analytic in analytics:
    #             if analytic.date == today:
    #                 if analytic.json_analytics:
    #                     vals = json.loads(analytic.json_analytics)
    #                 else:
    #                     vals = {
    #                         'posts': 0,
    #                         'feeds': 0,
    #                         'products': 0,
    #                     }
    #                 if 'is_clicked' in res:
    #                     if not res['is_clicked']:
    #                         vals['feeds'] += 1
    #                 if 'post_id' in res:
    #                     vals['posts'] += 1
    #                 if 'product_id' in res:
    #                     vals['products'] += 1
    #                 analytic.json_analytics = json.dumps(vals)
    #                 print(analytic.json_analytics)
    #                 check = 1
    #                 break
    #     if not check:
    #         vals = {
    #             'posts': 0,
    #             'feeds': 0,
    #             'products': 0,
    #         }
    #         if 'is_clicked' in res:
    #             if not res['is_clicked']:
    #                 vals['feeds'] += 1
    #         if 'post_id' in res:
    #             vals['posts'] += 1
    #         if 'product_id' in res:
    #             vals['products'] += 1
    #         analytic = request.env['analytics'].sudo().create({'feed_id': int(res['feed_id']),
    #                                                            'date': today,
    #                                                            'json_analytics': json.dumps(vals)})
    #         print(analytic)
    #         print(analytic.json_analytics)

    # @http.route('/instafeed/get/shopify', type='http', auth='public', csrf=False)
    def get_shopify_product(self, **kwargs):
        current_user = request.env.user
        store_info = request.env['shopify.store'].sudo().search([("admin", '=', current_user.id)], limit=1)
        new_session = shopify.Session(store_info.url, request.env['ir.config_parameter'].sudo().get_param(
            'instafeed.api_version_instafeed'),
                                      token=store_info.access_token)
        shopify.ShopifyResource.activate_session(new_session)
        products = shopify.Product.find()
        print(products)
        vals = []
        for product in products:
            vals.append({
                'product_id': product.id,
                'name': product.title,
                'url': f'{store_info.url}/products/{product.handle}',
                'shop_id': store_info.id,
                'price': float(product.variants[0].price),
                "compare_at_price": product.variants[0].compare_at_price,
                'qty': product.variants[0].inventory_quantity,
                "variant_id": product.variants[0].id,
                'image_url': product.image.src
            })
        return vals
