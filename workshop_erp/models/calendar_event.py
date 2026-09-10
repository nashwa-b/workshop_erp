# -*- coding: utf-8 -*-

from odoo import fields, models, api
from datetime import datetime, timedelta


class CalendarEvent(models.Model):
    _inherit = 'calendar.event'

    job_order_id = fields.Many2one('workshop.job.order', string='Job Order')
    customer_id = fields.Many2one(string='Customer', related='job_order_id.customer_id')

    def _send_remainder(self):
        """Send remainder email one day before scheduled appointment"""
        tomorrow = datetime.now() + timedelta(days=1)
        print(tomorrow)
        datee = self.search([('start','=',tomorrow)])
        # for record in self:
        # if 'start' == tomorrow:
        for event in datee:
                mail_template = self.env.ref('workshop_erp.mail_template_calendar_event')
                email_values = {'email_to': self.customer_id.email}

            # Send the template to each customer
                mail_template.send_mail(self.id, force_send=False, email_values=email_values)  # force_send=False queues the email

    # @api.model_create_multi
    def create(self, vals):
        res = super().create(vals)
        print(vals)
        # for record in self:
        #     print(record)
            # if 'some_field' in vals:
        template = self.env.ref('workshop_erp.mail_template_appointment_confirmation')
        email_values = {'email_to': self.job_order_id.customer_id.email}
        template.send_mail(self.id, force_send=True, email_values=email_values)
        return res


