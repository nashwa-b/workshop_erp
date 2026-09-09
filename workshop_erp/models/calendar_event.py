# -*- coding: utf-8 -*-

from odoo import fields, models


class CalendarEvent(models.Model):
    _inherit = 'calendar.event'

    job_order_id = fields.Many2one('workshop.job.order', string='Job Order')

    def action_view_appointment(self):
        """Open the vehicle view for this partner in smart button"""
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "calendar.event",
            "name": "Appointment",
            "views": [False, "list"],
            "domain": [('job_order_id', '=', self.job_order_id)],
        }

