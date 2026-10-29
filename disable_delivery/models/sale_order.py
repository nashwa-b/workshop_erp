# -*- coding: utf-8 -*-

from odoo import models


class SaleOrder(models.Model):
    """Extends sales model"""
    _inherit = 'sale.order'

    def action_confirm(self):
        """Create purchase order for each order line in sale order"""
        # if self.env.context.get("skip_procurement"):
        res = super(SaleOrder, self.with_context(skip_procurement=True)).action_confirm()
        return res

    def action_create_delivery(self):
        # context = self.env.context.copy()
        # sol = self.with_context(context)._action_confirm()
        # if self.env.context.get("skip_procurement"):
        self.order_line._action_launch_stock_rule()
        # print('s', sol)
        # return super(SaleOrder, self)._action_confirm()
        # return super(SaleOrder, self)._action_confirm()
        # return self.action_view_delivery()

    # def action_view_delivery(self):
    #     ew = self.action_view_delivery()

