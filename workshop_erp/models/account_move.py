# -*- coding: utf-8 -*-

from odoo import fields, models


class AccountMove(models.Model):
    """Extends partner model"""
    _inherit = ['account.move']

    job_order_id = fields.Many2one('workshop.job.order', string='Job Order')

    def action_post(self):
        """change status to invoiced when invoice is confirmed and assigning the invoice to invoice_id"""
        res = super(AccountMove, self).action_post()
        sale_orders = self.line_ids.sale_line_ids.order_id
        self.job_order_id = sale_orders.job_order_id
        self.job_order_id.write({'status':'invoiced','invoice_id':self.id})

        return res

