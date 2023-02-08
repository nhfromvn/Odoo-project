import json

from odoo import models, fields, api


class ContactXero(models.Model):
    _name = 'contact.xero'
    contact_id = fields.Char()