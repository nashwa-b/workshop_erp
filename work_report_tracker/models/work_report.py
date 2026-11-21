# -*- coding: utf-8 -*-

from odoo import fields, models, api,_
from odoo.tools import email_normalize


class WorkReport(models.Model):
    """workshop job types"""
    _name = 'work.report'
    _inherit = ['mail.thread.cc',
                'mail.thread.blacklist',
                'mail.thread.phone',
                'mail.activity.mixin',
                'utm.mixin',
                'format.address.mixin',
                'mail.tracking.duration.mixin',
                ]
    _primary_email = 'email_from'
    _description = 'Work Report'
    _rec_name = 'subject'

    subject = fields.Char(required=True)
    email_from = fields.Char(required=True)
    employee_id = fields.Char('hr.employee',required=True)
    body = fields.Html('body')
    date = fields.Datetime(string='Start Date')


    @api.model
    def message_new(self, msg_dict, custom_values=None):
        print("okjnhvgcx")
        print("msg_dict",msg_dict)

        self = self.with_context(default_user_id=False)
        email_address = email_normalize(msg_dict.get('email_from'))
        print(email_address)
        if not email_address:
            return self.env['hr.employee']

        employee = self.env['hr.employee'].search([
            ('work_email', '=ilike', email_address)
        ])
        print(employee)

        if custom_values is None:
            custom_values = {}
        defaults = {
            'subject': msg_dict.get('subject') or _("No Subject"),
            'email_from': employee.work_email,
            'employee_id': employee.name,
            'date': msg_dict.get('date'),
            'body': msg_dict.get('body'),
        }


        new_report = super().message_new(msg_dict, custom_values=defaults)
        # new_lead._assign_userless_lead_in_team(_('incoming email'))
        return new_report

    # @api.model
    # def _get_employee_from_email(self, email_address):
    #     if not email_address:
    #         return self.env['hr.employee']
    #     employee = self.env['hr.employee'].search([
    #         ('user_id', '!=', False), '|', ('work_email', 'ilike', email_address),
    #         ('user_id.email', 'ilike', email_address),
    #     ])
    #
    #     if len(employee) > 1:
    #         # Several employees can be linked to the same user.
    #         # In that case, we only keep the employee that matched the user's company.
    #         return employee.filtered(lambda e: e.company_id == e.user_id.company_id)

    # @api.model
    # def message_new(self, msg, custom_values=None):
    #     """ Overrides mail_thread message_new that is called by the mailgateway
    #         through message_process.
    #         This override updates the document according to the email.
    #     """
    #     # remove default author when going through the mail gateway. Indeed we
    #     # do not want to explicitly set user_id to False; however we do not
    #     # want the gateway user to be responsible if no other responsible is
    #     # found.
    #     if custom_values is None:
    #         custom_values = {}
    #     defaults = {
    #         'name': msg.get('subject') or _("No Subject"),
    #         'partner_id': msg.get('author_id')
    #     }
    #     defaults.update(custom_values)
    #     p_order = super(PurchaseOrder, self).message_new(msg, custom_values=defaults)
    #     return p_order

