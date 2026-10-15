# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ProductTemplate(models.Model):
    """Extends product template to display total sale count"""
    _inherit = 'product.template'

    total_sale_count = fields.Integer(compute='_compute_total_sale_count', string='Sale Count')

    def _compute_total_sale_count(self):
        """ Calculate total sale count """
        for record in self:
            sale_orders = self.env['sale.order'].search([('order_line.product_template_id', '=', record.id),('state','in',['sale','invoiced'])])
            record.total_sale_count = len(sale_orders)

    @api.onchange('list_price')
    def _onchange_list_price(self):
        """Change unit price of all sale order lines in draft state on changing the product's sale price"""
        sale_order_lines = self.env['sale.order.line'].search([('product_id', 'in', self.ids),('order_id.state','=', 'draft')])
        sale_order_lines.write({'price_unit': self.list_price})


