# -*- coding: utf-8 -*-

from odoo import models

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    def action_duplicate_sale_order(self):
        for order in self:
            new_order = order.copy()
            new_order.write({'state': 'draft'})