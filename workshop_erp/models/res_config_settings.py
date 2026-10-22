# -*- coding: utf-8 -*-

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    """Extends partner model by adding smart buttons for vehicles and job orders associated with that partner"""
    _inherit = 'res.config.settings'

    category_wise_discount = fields.Boolean(string="Enable Category-Wise Discount", default=True)

