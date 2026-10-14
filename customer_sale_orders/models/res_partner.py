# -*- coding: utf-8 -*-

from odoo import fields, models


class ResPartner(models.Model):
    """Extends customer form to add sale order page and product smart tab"""
    _inherit = 'res.partner'

    sale_order_ids = fields.One2many('sale.order', 'partner_id', string='Sales Orders')
    product_count = fields.Integer(compute='_compute_products', string='Product Count')

    def _compute_products(self):
        """Compute sales order product count"""
        for record in self:
            sale_orders = record.sale_order_ids.filtered(lambda order: order.state not in ['draft'])
            products = sale_orders.order_line.mapped('product_id')
            record.product_count = len(products)

    def action_view_products(self):
        """View Products in customer's sales order"""
        self.ensure_one()
        sale_orders = self.sale_order_ids.filtered(lambda order: order.state not in ['draft'])
        products = sale_orders.order_line.mapped('product_id')
        return {
            "type": "ir.actions.act_window",
            "res_model": "product.product",
            "name": "Products",
            "views": [[self.env.ref("product.product_product_tree_view").id, "list"]],
            "domain":[('id', 'in', products.ids)]
        }




