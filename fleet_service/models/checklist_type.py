# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.exceptions import ValidationError

class ChecklistType(models.Model):
    """Employee Loan"""
    _name = 'checklist.type'

    name = fields.Char(string="Name")