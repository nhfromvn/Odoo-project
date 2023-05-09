import json
from odoo import http, fields
from odoo.http import request
import hmac
import hashlib
import requests
import werkzeug
import os
import jinja2
from pytz import timezone
from datetime import datetime
import shopify, binascii, json, string, random

SCOPES = '''read_products,
          read_customers,
          write_customers,
          read_third_party_fulfillment_orders,
          write_third_party_fulfillment_orders,
          read_orders,
          write_orders,
          write_draft_orders,
          read_draft_orders,
          write_script_tags,
          read_shipping,
          read_themes,
          write_themes,
          read_price_rules'''


class InstafeedController(http.Controller):
    @http.route('/instafeed/install', auth='user')
    def install_instafeed(self, **kwargs):
        print(kwargs)
        shop_url = kwargs['shop']
        api_key = request.env['ir.config_parameter'].sudo().get_param('instafeed.api_key_instafeed')
        state = kwargs['hmac']
        callback = request.env['ir.config_parameter'].sudo().get_param(
            'web.base.url') + '/instafeed/oauth/callback'

        url = f"https://{shop_url}/admin/oauth/authorize?client_id={api_key}&scope={SCOPES}&redirect_uri={callback}&state={state}&grant_options[]=per-user"
        return werkzeug.utils.redirect(url)

    @http.route('/instafeed/oauth/callback', type="http", auth="public", website=True, method=['GET'], csrf=False)
    def instafeed_callback(self, **kwargs):
        if 'code' in kwargs:
            code = kwargs['code']

            if 'shop' in kwargs:
                shop_url = kwargs['shop']
            else:
                return json.dumps({
                    "error": "not found shop_url in response"
                })
            api_key = request.env['ir.config_parameter'].sudo().get_param('instafeed.api_key_instafeed')
            secret = request.env['ir.config_parameter'].sudo().get_param('instafeed.secret_key_instafeed')
            base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
            headers = {'Content-Type': 'application/json'}
            body = {
                "client_id": api_key,
                "client_secret": secret,
                "code": code
            }
            # try:
            vals = {}
            url = 'https://' + shop_url + '/admin/oauth/access_token'

            res = requests.post(url=url, headers=headers, data=json.dumps(body))
            if res.status_code == 200:
                data = res.json()
                request.session['shop_url'] = shop_url
                vals['first_name'] = data['associated_user']['first_name']
                vals['last_name'] = data['associated_user']['last_name']
                vals['shop_url'] = shop_url
                vals['email'] = data['associated_user']['email']
                vals['locale'] = data['associated_user']['locale']
                vals['access_token'] = data['access_token']
                vals['code'] = code
                store_exist = request.env['shop'].sudo().search([('shop_url', '=', shop_url)], limit=1)
                if store_exist:
                    store_exist.write(vals)
                else:
                    store_exist = request.env['shop'].sudo().create(vals)
                instafeed_user = request.env['instafeed'].sudo().search([('store_id', '=', store_exist.id)],
                                                                        limit=1)
                if not instafeed_user:
                    feed_exist = request.env['instafeed'].sudo().create({'store_id': store_exist.id})
                header = {
                    'X-Shopify-Access-Token': store_exist.access_token,
                    'Content-Type': 'application/json'
                }
                script_tags = requests.get(f"https://{shop_url}/admin/api/2023-01/script_tags.json",
                                           headers=header).json()
                if not script_tags['script_tags']:
                    req = requests.post(f"https://{shop_url}/admin/api/2023-01/script_tags.json",
                                        headers=header,
                                        json={"script_tag": {"event": "onload",
                                                             "src": request.env[
                                                                        'ir.config_parameter'].sudo().get_param(
                                                                 'web.base.url') + "/instafeed/static/js/extension.js"}})
                script_tags = requests.get(f"https://{shop_url}/admin/api/2023-01/script_tags.json",
                                           headers=header)
                print(str(script_tags.content))
                return werkzeug.utils.redirect(base_url + '/instafeed')
            # except Exception as e:
            #     print(e)
        else:
            return json.dumps({"error": "No code in response"})

    @http.route('/instafeed/save', type='json', auth="user")
    def save_feed(self, **kwargs):
        if request.httprequest.data:
            res = json.loads(request.httprequest.data)
            feed = res['feed']
            posts = res['posts']
            shop_url = request.session['shop_url']
            shop = request.env['shop'].sudo().search([('shop_url', '=', shop_url)], limit=1)
            instafeed_user = request.env['instafeed'].sudo().search([('store_id', '=', shop.id)], limit=1)
            facebook_user = request.env['facebook'].sudo().search([('feed_id', '=', instafeed_user.id)], limit=1)
            for post in posts:
                post_exist = request.env['instagram.post'].sudo().search(
                    [('facebook_id', '=', facebook_user.id), ('post_id', '=', post['id'])], limit=1)
                if post_exist:
                    for product in post_exist.products:
                        if product.product_id not in post['list_tags']:
                            post_exist.write({'products': [(3, request.env['shopify.product'].sudo().search(
                                [('product_id', '=', product.product_id), ('store_id', '=', shop.id)]).id)]})
                    for product_id in post['list_tags']:
                        product_exist = request.env['shopify.product'].sudo().search(
                            [('product_id', '=', product_id), ('store_id', '=', shop.id)])
                        if product_exist:
                            post_exist.write({'products': [(4, product_exist.id)]})
                        else:
                            product_exist = request.env['shopify.product'].sudo().create({
                                'product_id': product_id,
                                'store_id': shop.id,
                            })
                            post_exist.write({'products': [(4, product_exist.id)]})
                else:
                    post_exist = request.env['instagram.post'].sudo().create({
                        'facebook_id': facebook_user.id,
                        'post_id': post['id']
                    })
                    for product in post_exist.products:
                        if product.product_id not in post['list_tags']:
                            post_exist.write({'products': [(3, request.env['shopify.product'].sudo().search(
                                [('product_id', '=', product.product_id), ('store_id', '=', shop.id)]).id)]})
                    for product_id in post['list_tags']:
                        product_exist = request.env['shopify.product'].sudo().search(
                            [('product_id', '=', product_id), ('store_id', '=', shop.id)])
                        print(post_exist.id)
                        if product_exist:
                            post_exist.write({'products': [(4, product_exist.id)]})
                        else:
                            product_exist = request.env['shopify.product'].sudo().create({
                                'product_id': product_id,
                                'store_id': shop.id,
                            })
                            post_exist.write({'products': [(4, product_exist.id)]})
            if instafeed_user:
                instafeed_user.write(feed)
            else:
                feed['store_id'] = shop.id
                request.env['instafeed'].sudo().create(feed)
        else:
            return False

    @http.route('/instafeed/get/data', auth='user', csrf=False)
    def get_user_info(self, **kwargs):
        shop_url = request.session['shop_url']
        shop = request.env['shop'].sudo().search([('shop_url', '=', shop_url)], limit=1)
        instafeed_user = request.env['instafeed'].sudo().search([('store_id', '=', shop.id)], limit=1)
        enpoint = 'https://graph.instagram.com/me?fields=id,username&access_token=' + instafeed_user.access_token
        res = requests.get(enpoint)
        if res.ok:
            user = res.json()
            instafeed_user.write({'username': user['username']})
            media = self.get_media(instafeed_user)
            return json.dumps({'user': user,
                               'user_id': instafeed_user.user_id,
                               'media': media,
                               'feed_title': instafeed_user.feed_title,
                               'post_spacing': instafeed_user.post_spacing,
                               'on_post_click': instafeed_user.on_post_click,
                               'layout': instafeed_user.layout,
                               'configuration': instafeed_user.configuration,
                               'per_slide': instafeed_user.per_slide,
                               'number_of_posts': instafeed_user.number_of_posts,
                               'number_of_rows': instafeed_user.number_of_rows,
                               'number_of_columns': instafeed_user.number_of_columns,
                               'show_likes': instafeed_user.show_likes,
                               'show_followers': instafeed_user.show_followers,
                               })
        else:

            return False

    def get_media(self, instafeed_user):
        enpoint = 'https://graph.instagram.com/me/media?fields=id,caption,media_type,media_url,thumbnail_url,username,timestamp&access_token=' + instafeed_user.access_token
        res = requests.get(enpoint)
        if res.ok:
            return res.json()
        else:
            return False

    @http.route('/instafeed/get/fb-data', auth='user', csrf=False)
    def get_fb_data(self, **kwargs):
        shop_url = request.session['shop_url']
        shop = request.env['shop'].sudo().search([('shop_url', '=', shop_url)], limit=1)
        instafeed_user = request.env['instafeed'].sudo().search([('store_id', '=', shop.id)], limit=1)
        facebook_user = request.env['facebook'].sudo().search([('feed_id', '=', instafeed_user.id)])
        enpoint = 'https://graph.facebook.com/v12.0/me?fields=id,name,accounts&access_token=' + facebook_user.access_token
        res = requests.get(enpoint)
        if res.ok:
            user = res.json()
            insta_business_id = self.get_insta_business(user['accounts']['data'][0]['id'], facebook_user)
            instagram_info = self.get_info(insta_business_id, facebook_user)
            vals = {'fb_username': user['name'],
                    'page_id': user['accounts']['data'][0]['id'],
                    'instagram_business_account_id': insta_business_id,
                    'followers_count': instagram_info['followers_count'],
                    }
            for post in instagram_info['media']['data']:
                post_exist = request.env['instagram.post'].sudo().search(
                    [('post_id', '=', post['id']), ('facebook_id', '=', facebook_user.id)], limit=1)
                if post_exist:
                    post_exist.write({'facebook_id': facebook_user.id,
                                      'post_id': post['id']})
                    list = []
                    for product in post_exist.products:
                        list.append(product.product_id)
                        post['list_tags'] = list
                else:
                    post_exist = request.env['instagram.post'].sudo().create({
                        'facebook_id': facebook_user.id,
                        'post_id': post['id']
                    })
            facebook_user.write(vals)
            vals['media'] = instagram_info['media']
            return json.dumps(vals)

    def get_insta_business(self, page_id, facebook_user):
        enpoint = 'https://graph.facebook.com/v12.0/' + page_id + '?fields=instagram_business_account&access_token=' + facebook_user.access_token
        res = requests.get(enpoint)
        if res.ok:
            account = res.json()
        facebook_user.write({'instagram_business_account_id': account['instagram_business_account']['id']})
        return res.json()['instagram_business_account']['id']

    def get_info(self, insta_business_id, facebook_user):
        enpoint = 'https://graph.facebook.com/v12.0/' + insta_business_id + '?fields=name,username,followers_count,media{id,caption,media_type,media_url,thumbnail_url,username,permalink,timestamp,comments_count,comments{from,text},like_count}&access_token=' + facebook_user.access_token
        res = requests.get(enpoint)
        if res.ok:
            account = res.json()
        return res.json()

    @http.route('/instafeed/show/feed', type='json', auth='public', csrf=False)
    def show_feed(self, **kwargs):
        res = json.loads(request.httprequest.data)
        shop_url = res['shop_url']
        shop = request.env['shop'].sudo().search([('shop_url', '=', shop_url)], limit=1)
        instafeed_user = request.env['instafeed'].sudo().search([('store_id', '=', shop.id)], limit=1)
        facebook_user = request.env['facebook'].sudo().search([('feed_id', '=', instafeed_user.id)])
        enpoint = 'https://graph.instagram.com/me?fields=id,username&access_token=' + instafeed_user.access_token
        res = requests.get(enpoint)
        products = json.loads(self.sync_product(shop_url))
        print(products)
        vals = []
        for product in products['products']:
            vals.append({
                'product_id': product['id'],
                'name': product['title'],
                'handle': product['handle'],
                'image_url': product['image']['src']
            })
        if res.ok:
            user = res.json()
            instafeed_user.write({'username': user['username']})
            business_info = self.get_info(facebook_user.instagram_business_account_id, facebook_user)
            for post in business_info['media']['data']:
                post_exist = request.env['instagram.post'].sudo().search(
                    [('post_id', '=', post['id']), ('facebook_id', '=', facebook_user.id)], limit=1)
                if post_exist:
                    post_exist.write({'facebook_id': facebook_user.id,
                                      'post_id': post['id']})
                    list = []
                    for product in post_exist.products:
                        list.append(product.product_id)
                        post['list_tags'] = list
                else:
                    post_exist = request.env['instagram.post'].sudo().create({
                        'facebook_id': facebook_user.id,
                        'post_id': post['id']
                    })
            return {'user': user,
                    'user_id': instafeed_user.user_id,
                    'media': business_info['media'],
                    'feed_title': instafeed_user.feed_title,
                    'post_spacing': instafeed_user.post_spacing,
                    'on_post_click': instafeed_user.on_post_click,
                    'layout': instafeed_user.layout,
                    'configuration': instafeed_user.configuration,
                    'per_slide': instafeed_user.per_slide,
                    'number_of_posts': instafeed_user.number_of_posts,
                    'number_of_rows': instafeed_user.number_of_rows,
                    'number_of_columns': instafeed_user.number_of_columns,
                    'show_likes': instafeed_user.show_likes,
                    'show_followers': instafeed_user.show_followers,
                    'followers_count': business_info['followers_count'],
                    'products': vals
                    }
        else:
            return False

    @http.route('/instafeed/get/shopify', type='http', auth='public', csrf=False)
    def get_shopify(self, **kwargs):
        shop_url = request.session['shop_url']
        store_info = request.env['shop'].sudo().search([('shop_url', '=', shop_url)], limit=1)
        if self.sync_product(shop_url):
            products = json.loads(self.sync_product(shop_url))
        else:
            return json.dumps({
                "error": "Exception error"
            })
        if products:
            list_products = []
            for product in products['products']:
                vals = {}

                product_exist = request.env['shopify.product'].sudo().search([('product_id', '=', str(product['id']))],
                                                                             limit=1)
                vals['product_id'] = product['id']
                vals['store_id'] = store_info.id
                vals['name'] = product['title']
                vals['handle'] = product['handle']
                vals['price'] = product['variants'][0]['price']
                vals['variant_id'] = product['variants'][0]['id']
                if not product['image'] == None:
                    vals['image_url'] = product['image']['src']
                else:
                    vals['image_url'] = '/bought_together/static/app/img/img_3.png'
                vals['compare_at_price'] = product['variants'][0]['compare_at_price']
                vals['qty_in_stock'] = product['variants'][0]['inventory_quantity']
                if product_exist:
                    product_exist.sudo().write(vals)
                else:
                    product_exist.sudo().create(vals)
                list_products.append(vals)
            return json.dumps({"products": list_products,
                               "shop_url": shop_url})
        else:
            return False

    def sync_product(self, shop_url):
        store_info = request.env['shop'].sudo().search([('shop_url', '=', shop_url)], limit=1)
        if store_info:
            access_token = store_info.access_token
            header = {
                'X-Shopify-Access-Token': access_token,
            }
            response = requests.get("https://" + shop_url + '/admin/api/2023-01/products.json', headers=header,
                                    params={})
            if response.ok:
                return json.dumps(response.json())
            else:
                return False
        else:
            return False
