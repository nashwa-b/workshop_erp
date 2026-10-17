# -*- coding: utf-8 -*-

from odoo import fields, models


class HrEmployee(models.Model):
    """Extend hr employee to add loan not allowed field"""
    _inherit = 'hr.employee'

    loan_not_allowed = fields.Boolean(string="Loan Not Allowed")