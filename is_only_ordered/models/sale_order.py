# -*- coding: utf-8 -*-

from odoo import models


class SaleOrder(models.Model):
    """Extends sales model"""
    _inherit = 'sale.order'

    def action_confirm(self):
        """Create purchase order for each order line in sale order"""
        res = super(SaleOrder, self).action_confirm()
        print('l',self)
        if self.partner_id.is_only_ordered:



            invoice = self.env["ir.actions.actions"]._for_xml_id("sale.action_view_sale_advance_payment_inv")


            confirm = self.env['account.move'].search([('invoice_origin','=',self.id)])
            print('a',confirm)
            confirm.action_post()

            return invoice
        return res





            # print('o',invoices)

            # i = self.invoice_ids
            # print('l',i)
            # print('a',invoice,confirm)
            # return invoice,confirm

        # self.action_post()
        return res

    # < button
    # string = "Create Invoices"
    # name = "%(sale.action_view_sale_advance_payment_inv)d"
    # type = "action"
    #
    # class ="btn-secondary" / >