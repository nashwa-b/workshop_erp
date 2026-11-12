# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.exceptions import ValidationError

class FleetServiceOrderChecklist(models.Model):
    """Employee Loan"""
    _name = 'fleet.service.order.checklist'
    _description = 'Fleet Service Order Checklist'

    order_id = fields.Many2one('fleet.service.order')
    task_name = fields.Char(string="Task Name")
    is_done = fields.Boolean(string="Is Done")
    note = fields.Text(string="Note")

