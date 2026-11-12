# -*- coding: utf-8 -*-

from odoo import models

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    def action_duplicate_sale_order(self):
        for order in self:
            new_order = order.copy()
            new_order.write({'state': 'draft'})

            # from odoo import models, api
            # class SaleOrder(models.Model):
            #     _inherit = 'sale.order'  # Inherit the sale.order model
            #
            #     def action_confirm(self):
            #         # Call the original confirm method
            #         res = super(SaleOrder, self).action_confirm()
            #         # Add a display notification
            #         return {
            #             'type': 'ir.actions.client',
            #             'tag': 'display_notification',
            #             'params': {
            #                 'title': 'Order Confirmed!',
            #                 'message': f'Sale Order {self.name} has been successfully confirmed.',
            #                 'type': 'success',  # Blue success notification,
            #                 'sticky': False,  # Auto-dismiss after a few seconds
            #             }
            #         }
