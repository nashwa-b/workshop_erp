# -*- coding: utf-8 -*-

from odoo import fields, models, api,_,tools
from odoo.tools import email_normalize
from bs4 import BeautifulSoup


class WorkReport(models.Model):
    """workshop job types"""
    _name = 'work.report'
    _inherit = 'mail.thread.blacklist'
    _primary_email = 'email_from'
    _description = 'Work Report'
    # _rec_name = 'subject'

    subject = fields.Char(required=True)
    email_from = fields.Char(required=True)
    name = fields.Many2one('hr.employee',string="Employee")
    body = fields.Html('body')
    date = fields.Datetime(string='Date')
    project = fields.Char('project')
    remarks = fields.Char(string="Remarks")


    @api.model
    def message_new(self, msg_dict, custom_values=None):
        """create new report record from email"""
        print("msg_dict",msg_dict)

        email_address = email_normalize(msg_dict.get('email_from'))
        print(email_address)
        # if not email_address:
        #     return self.env['hr.employee']

        employee = self.env['hr.employee'].search([
            ('work_email', '=ilike', email_address)
        ], limit=1)

        # employees = self.env['hr.employee'].search_read([('work_email', '=ilike', email_address)],
        #     fields=['id'],limit=1
        # )
        # print(employees)
        # print(employees[0]['id'])
        vals = {}


        if custom_values is None:
            custom_values = {}


        html_body = msg_dict.get('body')
        soup = BeautifulSoup(html_body, 'html.parser')

        rows = soup.find_all('tr')
        print("rows",rows)

        second_row = rows[2]
        data = [td.get_text(strip=True) for td in second_row.find_all('td')]
        print('values',data)
        print('values[0]',data[1])
        pro_name = data[1]
        remarks = data[4]


        body_text = tools.html2plaintext(msg_dict.get('body'))
        print("text",body_text)


        lines = body_text.split('\n')
        print('line2',lines[2])
        label = lines[2].strip().lower()

        parts = label.split(' ')
        print('parts',parts)

        words = parts[2].split("<td>")
        print("word2",words)

        print('ll',self.project)

        # project = words[2]
        # print('project3',project)

        # words = parts[2].split("<td>")
        project_name = words[0].strip() if words else ""
        print('project_name',project_name)



        defaults = {
            'subject': msg_dict.get('subject') or _("No Subject"),
            'email_from': email_address,
            'name': employee.id if employee else None,
            'date': msg_dict.get('date'),
            'body': msg_dict.get('body'),
            "project": pro_name,
            "remarks": remarks,

        }



        new_report = super().message_new(msg_dict, custom_values=defaults)
        # new_lead._assign_userless_lead_in_team(_('incoming email'))
        return new_report




