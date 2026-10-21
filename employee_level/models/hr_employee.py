# -*- coding: utf-8 -*-

from odoo import fields, models, api


class HrEmployee(models.Model):
    """Extends hr employee to add salary levels"""
    _inherit = 'hr.employee'

    employee_level_id = fields.Many2one('employee.level', string="Employee Level")
    salary = fields.Float(string="Salary", related="employee_level_id.salary")
    is_higher = fields.Boolean(related="employee_level_id.is_max_level")
    # is_click = fields.Boolean(string="Is Click", default=False)

    def action_promote(self):
        """ Increase level and salary and hides button if level is highest """
        record = self.env['employee.level'].search([('level', '>', self.employee_level_id.id)], order='level asc',
                                                   limit=1)
        if record:
            self.employee_level_id = record.id
            self.salary = record.salary
            # rec = self.env['employee.level'].search_count([('level', '>', self.employee_level_id.id)])
            # if rec == 0:
            #     self.is_click = True
