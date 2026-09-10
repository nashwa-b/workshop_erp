# -*- coding: utf-8 -*-

from odoo import fields, models


class SaleOrder(models.Model):
    """Extends sales model"""
    _inherit = 'sale.order'

    job_order_id = fields.Many2one('workshop.job.order',
                                   string='Job Order',
                                   copy=True, bypass_search_access=True)
    vehicle_id = fields.Many2one(string='Vehicle', related='job_order_id.vehicle_id')

    def action_confirm(self):
        """change status of job order to confirmed when quotation is confirmed """
        res = super(SaleOrder, self).action_confirm()
        self.job_order_id.status = 'confirmed'
        print(self.job_order_id)
        return res

    # def action_create_payments(self):
    #     res = super(SaleOrder, self).action_create_payments()
    #     mail_template = self.env.ref('workshop_erp.mail_template_vehicle_pickup')
    #     email_values = {'email_to': self.job_order_id.customer_id.email}
    #
    #     # Send the template to each customer
    #     mail_template.send_mail(self.id, force_send=False,
    #                             email_values=email_values)
    #     return res


