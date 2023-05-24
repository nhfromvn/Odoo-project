from odoo import api, fields, models
import os
from datetime import datetime


class AnalyticsPost(models.Model):
    _name = 'analytics'
    date = fields.Date()
    json_analytics = fields.Char()
    feed_id = fields.Many2one('widget.data')

    @staticmethod
    def run():
        os.system("echo 'Test Cron: %s' > /tmp/test.txt" % datetime.now())
        print('test cronjob')