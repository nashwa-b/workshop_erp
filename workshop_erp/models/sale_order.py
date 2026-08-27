# -*- coding: utf-8 -*-

from odoo import fields, models


class SaleOrder(models.Model):
    """Extends sales model"""
    _inherit = 'sale.order'

    job_order_id = fields.Many2one('workshop.job.order',
                                   string='Job Order',
                                   copy=True, bypass_search_access=True)
    # job_order_ids = fields.One2many(
    #     comodel_name='workshop.job.order', inverse_name='bay_id')
    vehicle_id = fields.Many2one(string='Vehicle', related='job_order_id.vehicle_id')
