# -*- coding: utf-8 -*-

from odoo import fields, models,api


class ProductProduct(models.Model):
    """Extend product variants view to display average cost of that product from all purchase orders"""
    _inherit = 'product.product'

    average_cost = fields.Float(compute = "_compute_average_cost",string='Average Cost')

    def _compute_average_cost(self):
        """compute average cost from all purchase orders"""
        for record in self:
           lines =  self.env['purchase.order.line'].search([('product_id', '=', record.id),('order_id.state','=','purchase')])
           total_amount = 0
           total_qty = 0
           total_amount = sum(lines.mapped('price_subtotal'))
           total_qty = sum(lines.mapped('product_qty'))
           if total_qty:
               record.average_cost = (total_amount/total_qty)
               print("k",record.average_cost)
           else:
               record.average_cost = 0