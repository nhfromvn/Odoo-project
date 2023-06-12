from odoo import fields, api, models
import requests
from odoo.http import request
import shopify


class SocialAccount(models.Model):
    _name = 'social.account'
    username = fields.Char()
    admin = fields.Many2one('res.users')
    url_image = fields.Char()
    access_token = fields.Char()
    user_id = fields.Char()
    status = fields.Boolean()
    instagram_business_account_id = fields.Char()
    instagram_business_account_username = fields.Char()
    instagram_business_account_followers_count = fields.Char()
    posts = fields.One2many('post.private', 'social_account')
    type = fields.Char(default=False)
    rapid_id = fields.Char()

    def get_data(self):
        if self.type == 'facebook':
            current_user = request.env.user
            enpoint = 'https://graph.facebook.com/v12.0/' + self.instagram_business_account_id + '?fields=name,username,followers_count,media{id,caption,media_type,media_url,thumbnail_url,username,permalink,timestamp,comments_count,like_count}&access_token=' + self.access_token
            res = requests.get(enpoint).json()
            self.write({
                'instagram_business_account_username': res['username'],
                'instagram_business_account_followers_count': res['followers_count']
            })
            for post in res['media']['data']:
                exist_post = self.env['post.private'].sudo().search(
                    [('post_id', "=", post['id']), ('admin', '=', current_user.id), ('social_account', '=', self.id)])
                post_data = {
                    'admin': current_user.id,
                    'media_url': post['media_url'],
                    'caption': post.get('caption') if 'caption' in post else None,
                    "post_id": post['id'],
                    "social_account": self.id,
                    "like_count": post['like_count'],
                    'type': post['media_type'],
                    "link_to_post": post['permalink'],
                    'thumbnail_url': post.get('thumbnail_url') if 'thumbnail_url' in post else None,
                    'comments_count': post['comments_count'],
                }
                if exist_post:
                    exist_post.sudo().write(post_data)
                else:
                    exist_post = self.env['post.private'].sudo().create(post_data)
        elif self.type == 'instagram':
            current_user = request.env.user
            enpoint = 'https://graph.instagram.com/v12.0/me?fields=profile_picture_url,name,username,media{id,caption,media_type,media_url,thumbnail_url,username,timestamp,permalink}&access_token=' + self.access_token
            res = requests.get(enpoint).json()
            self.username = res['username']
            for post in res['media']['data']:
                exist_post = self.env['post.private'].sudo().search(
                    [('post_id', "=", post['id']), ('admin', '=', current_user.id), ('social_account', '=', self.id)])
                post_data = {
                    'admin': current_user.id,
                    'media_url': post['media_url'],
                    'caption': post.get('caption') if 'caption' in post else None,
                    "post_id": post['id'],
                    "social_account": self.id,
                    "link_to_post": post['permalink'],
                    'type': post['media_type'],
                    'thumbnail_url': post.get('thumbnail_url') if 'thumbnail_url' in post else None,
                }
                if exist_post:
                    exist_post.sudo().write(post_data)
                else:
                    exist_post = self.env['post.private'].sudo().create(post_data)
        elif self.type == 'tiktok':
            current_user = request.env.user
            shop = request.env['shopify.store'].sudo().search([('admin', '=', current_user.id)])
            new_session = shopify.Session(shop.url, request.env['ir.config_parameter'].sudo().get_param(
                'instafeed.api_version_instafeed'),
                                          token=shop.access_token)

            shopify.ShopifyResource.activate_session(new_session)
            theme_id = shopify.Theme.find()[0].id
            enpoint = 'https://open-api.tiktok.com/user/info/'

            param = {
                'access_token': self.access_token,
                'fields': ["open_id", "union_id", "avatar_url", "display_name"]
            }
            res = requests.post(enpoint, json=param).json()
            self.write({
                'user_id': res['data']['user']['open_id'],
                'url_image': res['data']['user']['avatar_url'],
                'username': res['data']['user']['display_name']
            })
            print(res)
            new_enppont = 'https://open-api.tiktok.com/video/list/'
            new_param = {
                'access_token': self.access_token,
                'fields': ["id", "like_count", "embed_link", "embed_html", "comment_count", "video_description",
                           "share_url", "cover_image_url"]
            }

            new_res = requests.post(new_enppont, json=new_param).json()
            print(new_res)
            if self.rapid_id:
                videos = self.rapid_api_get_videos()['data']['videos']
            else:
                self.rapid_api_get_id()
                videos = self.rapid_api_get_videos()['data']['videos']
            print(videos)
            for video in videos:
                asset = shopify.Asset.create({
                    "theme_id": int(theme_id),
                    "key": f"assets/{video['video_id']}.mp4",
                    "src": video["wmplay"]
                })
                video['url'] = asset.public_url
            for post in new_res['data']['videos']:
                exist_post = self.env['post.private'].sudo().search(
                    [('post_id', "=", post['id']), ('admin', '=', current_user.id), ('social_account', '=', self.id)])
                post_data = {
                    'admin': current_user.id,
                    # 'media_url': response['video'][0],
                    'caption': post.get('video_description') if 'video_description' in post else None,
                    "post_id": post['id'],
                    "social_account": self.id,
                    "link_to_post": post['share_url'],
                    'type': 'VIDEO',
                    'thumbnail_url': post.get('cover_image_url') if 'cover_image_url' in post else None,
                    "like_count": post['like_count'],
                    'comments_count': post['comment_count'],
                    'tiktok': True
                }

                if exist_post:
                    exist_post.sudo().write(post_data)
                else:
                    exist_post = self.env['post.private'].sudo().create(post_data)
                for video in videos:
                    if video['video_id'] == exist_post.post_id:
                        exist_post.media_url = video['url']
                        print(exist_post.media_url)

    def rapid_api_get_id(self):
        if self.type == 'tiktok':
            url = "https://tiktok-video-no-watermark2.p.rapidapi.com/user/search"

            querystring = {"keywords": self.username, "count": "1", "cursor": "0"}

            headers = {
                "X-RapidAPI-Key": "df3ed756d2mshf054017e73cbe03p12e4ccjsn56d3ff5bfd4c",
                "X-RapidAPI-Host": "tiktok-video-no-watermark2.p.rapidapi.com"
            }

            response = requests.get(url, headers=headers, params=querystring)

            print(response.json())
            self.rapid_id = response.json()['data']['user_list'][0]['user']['id']
            return response.json()

    def rapid_api_get_videos(self):
        if self.type == 'tiktok':
            url = "https://tiktok-video-no-watermark2.p.rapidapi.com/user/posts"

            querystring = {"unique_id": "@tiktok", "user_id": self.rapid_id, "count": "10", "cursor": "0"}

            headers = {
                "X-RapidAPI-Key": "df3ed756d2mshf054017e73cbe03p12e4ccjsn56d3ff5bfd4c",
                "X-RapidAPI-Host": "tiktok-video-no-watermark2.p.rapidapi.com"
            }

            response = requests.get(url, headers=headers, params=querystring)

            print(response.json())
            return response.json()
