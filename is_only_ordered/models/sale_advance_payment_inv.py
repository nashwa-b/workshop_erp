# -*- coding: utf-8 -*-

from odoo import models


class SaleAdvancePaymentInv(models.TransientModel):
    _inherit = 'sale.advance.payment.inv'

    def _create_invoices(self, sale_orders):
        confirm = self.env['account.move'].search([('invoice_origin', '=', self.id)])
        print('a', confirm)
        self.action_post()

        return super()._create_invoices(sale_orders)

