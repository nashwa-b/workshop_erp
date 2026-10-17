# -*- coding: utf-8 -*-

from odoo import fields, models


class SaleOrderLine(models.Model):
    """Extends sales model to import lines"""
    _inherit = 'sale.order.line'

    milestone  = fields.Integer(string="Milestone")