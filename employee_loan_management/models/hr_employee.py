# -*- coding: utf-8 -*-

from odoo import fields, models


class ResUsers(models.Model):
    """Extend res user to create transfer request"""
    _inherit = 'hr.employee'

    loan_not_allowed = fields.Boolean(string="Not Allowed")