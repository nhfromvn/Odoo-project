from odoo import models, fields, api


class my_project(models.Model):
    _name = 'project.task'
    _description = 'my_project.my_project'
    stage_id = fields.Text()
    user_id= fields.Text()
    date_assign = fields.Date(string='Date assign')
    date_end = fields.Date(string ='Date end')
    project_id = fields.Text()
    name = fields.Char()
    value = fields.Integer()
    value2 = fields.Float(compute="_value_pc", store=True)
    description = fields.Text()

    @api.depends('value')
    def _value_pc(self):
        for record in self:
            record.value2 = float(record.value) / 100