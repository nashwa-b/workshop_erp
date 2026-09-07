# -*- coding: utf-8 -*-

from odoo import fields, models

class JobType(models.Model):
    """workshop job order"""
    _name = 'job.type'

    name = fields.Char(string='Job Type')