# -*- coding: utf-8 -*-

from odoo import fields, models


class SaleOrderLine(models.Model):
    """Extends sale order line model to add milestone tasks"""
    _inherit = 'sale.order.line'

    milestone  = fields.Integer(string="Milestone")