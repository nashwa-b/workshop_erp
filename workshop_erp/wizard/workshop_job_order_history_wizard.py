# -*- coding: utf-8 -*-

from odoo import fields, models

# import io
# from datetime import datetime, date
# from dateutil.rrule import rrule, DAILY
# from odoo.exceptions import ValidationError
# from odoo.tools import date_utils, json_default
# import json


class WorkshopJobOrderHistoryWizard(models.TransientModel):
    """Creation of Wizard for employee transfer"""
    _name = 'workshop.job.order.wizard'
    _description = 'Job Order History'

    customer_id = fields.Many2one('res.partner', string="Customer")
    vehicle_id = fields.Many2one('workshop.vehicle', string="Vehicle")
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")
    detailed_view = fields.Boolean(string="Detailed View")

    def action_report_job_order(self):
        return self.env.ref('workshop_erp.action_report_joborder').report_action(self)

    # def action_print_xlsx(self):
    #     data = {
    #         'from_date': self.start_date,
    #         'end_date': self.end_date,
    #         'vehicle_id': self.vehicle_id.id,
    #         'customer_id': self.customer_id.id,
    #
    #     }
    #     return {
    #         'type': 'ir.actions.report',
    #         'data': {'model': 'workshop.job.order.wizard',
    #                  'options': json.dumps(data, default=json_default),
    #                  'output_format': 'xlsx',
    #                  'report_name': 'Attendance Report',
    #                  },
    #         'report_type': 'xlsx',
    #     }
