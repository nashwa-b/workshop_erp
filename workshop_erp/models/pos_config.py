# -*- coding: utf-8 -*-

from odoo import models, fields


class PosConfig(models.Model):
    """Extends pos.config to add new boolean to validate max discount given in pos category"""
    _inherit = 'pos.config'

    category_wise_discount = fields.Boolean(string="Enable Category-Wise Discount")

