# -*- coding: utf-8 -*-

from odoo import fields, models

class WorkReportLines(models.Model):
    """Work Report Lines"""
    _name = 'work.report.lines'
    _description = 'Work Report Lines'

    report_id = fields.Many2one(
        'work.report'
    )
    project_id = fields.Many2one('project.project',
        string='Project')
    task = fields.Char()
    remarks = fields.Text()
