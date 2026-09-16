# -*- coding: utf-8 -*-

from odoo import fields, models, api


class SaleOrder(models.Model):
    """Extends sales model"""
    _inherit = 'sale.order'

    associated_products = fields.Boolean(string='Associated Products')

    @api.onchange('associated_products')
    def _onchange_associated_products(self):
        """fill and delete the order lines of SO with associated products of partner when enabling and disabling the boolean field"""
        product = self.partner_id.associated_product_ids
        if self.associated_products:
            self.order_line = [fields.Command.create(
                {'product_id': i.id,
                 'product_uom_qty': 1,
                 'price_unit': i.list_price}) for i in product]
        else:
            order_lines = self.order_line.filtered(lambda line:line.product_id.id in product.ids)
            self.order_line -= order_lines
            # order_lines.unlink()
            # for line in self.order_line:
            #     if line.product_id.id in product.ids:
            #         self.order_line = [fields.Command.delete(line.id)]

            # lines_to_recompute = self.order_line.filtered(lambda line: not line.display_type)






