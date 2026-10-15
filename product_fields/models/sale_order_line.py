# -*- coding: utf-8 -*-

from odoo import fields, models, api


class SaleOrderLine(models.Model):
    """Extends sale order line to add new field brand"""
    _inherit = 'sale.order.line'

    product_brand_id = fields.Many2one('product.brand', string='Brand', related = 'product_id.product_brand_id')
    allowed_product_ids = fields.Many2many('product.product')
    
    @api.onchange('product_id')
    def _onchange_product_id(self):
        """To filter products in sale order line according to boolean field in res partner"""
        print(self)
        if self.order_id.partner_id.is_prime_customer:
            products = self.env['product.product'].search([('product_master_type', '=', 'branded_product')])
            self.allowed_product_ids = products
        else:
            products = self.env['product.product'].search([])
            self.allowed_product_ids = products




