# -*- coding: utf-8 -*-

from odoo import models


class SaleOrder(models.Model):
    """Extends sales model"""
    _inherit = 'sale.order'

    def action_confirm(self):
        """Create Invoice during confirmation"""
        res = super(SaleOrder, self).action_confirm()
        print('l',self)
        if self.partner_id.is_only_ordered:
            invoice = self.env["ir.actions.actions"]._for_xml_id("sale.action_view_sale_advance_payment_inv")
        #     invoice = self._create_invoices()
        #     if invoice:
        #         invoice.action_post()
            return invoice
        return res