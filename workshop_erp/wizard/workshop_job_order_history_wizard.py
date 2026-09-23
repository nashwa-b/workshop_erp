# -*- coding: utf-8 -*-

from odoo import fields, models


class WorkshopJobOrderHistoryWizard(models.TransientModel):
    """Creation of Wizard for employee transfer"""
    _name = 'workshop.job.order.wizard'
    _description = 'Job Order History'

    customer_id = fields.Many2one('res.partner', string="Customer")
    vehicle_id = fields.Many2one('workshop.vehicle', string="Vehicle")
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")

    def action_report_job_order(self):
        return self.env.ref('workshop_erp.action_report_joborder').report_action(self)
