# -*- coding: utf-8 -*-

from odoo import fields, models
from odoo.tools import json_default
import json


class WorkReportWizard(models.TransientModel):
    """Creation of Wizard for work report"""
    _name = 'work.report.wizard'
    _description = 'Work Report Wizard'

    employee_id = fields.Many2one('hr.employee', string="Employee")
    project = fields.Char(string="Project")
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")

    def action_print_work_report(self):
        """pdf report action"""
        return self.env.ref('work_report_tracker.action_report_work_history').report_action(self)

