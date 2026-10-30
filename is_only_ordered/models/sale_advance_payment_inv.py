# -*- coding: utf-8 -*-

from odoo import models


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = 'sale.advance.payment.inv'

    def create_invoices(self):
        """Confirm Invoice"""

        res = super(SaleAdvancePaymentInv, self).create_invoices()
        sale_order = self.env['sale.order'].browse(self.env.context.get('active_ids',[]))
        print("oo",sale_order)

        for order in sale_order:
            if order.partner_id.is_only_ordered:
                invoice = self.env['account.move'].search([('invoice_origin', '=', order.name),('move_type', '=', 'out_invoice'),('state', '=', 'draft')])
            print('lkj',invoice)
            invoice.action_post()

        return res


