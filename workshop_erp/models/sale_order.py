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
        res = super(SaleOrder, self).action_confirm()
        self.job_order_id.status = 'confirmed'
        print(self.job_order_id)
        return res

