# -*- coding: utf-8 -*-

from odoo import fields, models


class ApprovalBlock(models.Model):
    _name = 'approval.block'
    _rec_name = 'limit'

    name = fields.Char(string="Name")
    limit = fields.Float("Limit")