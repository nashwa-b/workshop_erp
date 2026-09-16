# -*- coding: utf-8 -*-

from odoo import fields, models


class ProductTemplate(models.Model):
    """Adding sale order button in product view"""
    _inherit = 'product.template'


    def action_open_sale_order_wizard(self):
        """ Open the sale order wizard """
        self.ensure_one()
        print(self)
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sale Order Wizard',
            'res_model': 'sale.order.wizard',
            "views": [[self.env.ref('automated_sale_order.view_sales_order_wizard_form').id, "form"]],
            'target': 'new',
            'context': {'default_product_id': self.id, 'default_price_unit':self.list_price}
        }


