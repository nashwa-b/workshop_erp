# -*- coding: utf-8 -*-

from odoo import fields, models, api


class SaleOrderLine(models.Model):
    """Extends sale order line to add new field brand"""
    _inherit = 'sale.order.line'

    allowed_products_ids = fields.Many2many('product.product')

    @api.onchange('product_id')
    def _onchange_product_id(self):
        """To filter products in sale order line according to boolean field in res partner"""
        print(self)
        if self.order_id.partner_id.is_only_ordered:
            products = self.env['product.product'].search([('invoice_policy', '=', 'order')])
            self.allowed_products_ids = products
        else:
            products = self.env['product.product'].search([])
            self.allowed_products_ids = products
