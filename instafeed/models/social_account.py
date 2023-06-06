from odoo import fields, api, models
import requests
from odoo.http import request


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

