# -*- coding: utf-8 -*-

from odoo import fields, models


class ApprovalBlock(models.Model):
    _name = 'approval.block'

    name = fields.Char(string="Name")
    limit = fields.Float("limit")