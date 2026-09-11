# -*- coding: utf-8 -*-

from odoo import fields, models, api
from datetime import datetime, timedelta, time


class CalendarEvent(models.Model):
    _inherit = 'calendar.event'

    job_order_id = fields.Many2one('workshop.job.order', string='Job Order')
    # customer_id = fields.Many2one(string='Customer', related='job_order_id.customer_id')

    def _send_remainder(self):
        """Send remainder email one day before scheduled appointment"""
        tomorrow = datetime.now() + timedelta(days=1)
        print(tomorrow)
        # print(tomorrow.strftime('%y-%m-%d'))
        # tom = tomorrow.strftime('20%y-%m-%d')
        day_start = datetime.combine(tomorrow, time.min)
        day_end = datetime.combine(tomorrow, time.max)
        print(day_start, day_end)
        print("Sfd", self)
        # record = self.search([('start','in',tom)])
        record = self.search([('start','>=',day_start),('start','<=',day_end)])
        # record = self.search([('name','=',"jj")])
        # for i in record:
        #     print("fxfd", i, i.start)
        print("jj",record)
        for rec in record:
            print(rec.id)
            print(rec.customer_id.name)
            mail_template = self.env.ref('workshop_erp.mail_template_calendar_event')
            email_values = {'email_to': rec.customer_id.email}
            mail_template.send_mail(rec.id, force_send=True, email_values=email_values) # force_send= False queues the email

    @api.model_create_multi
    def create(self, vals_list):
        """Send appointment confirmation email when appointment is created"""
        res = super().create(vals_list)
        print(res)
        print(res.job_order_id.customer_id.name)
        template = self.env.ref('workshop_erp.mail_template_appointment_confirmation')
        email_values = {'email_to': res.job_order_id.customer_id.email}
        template.send_mail(res.id, force_send=True, email_values=email_values)
        return res


