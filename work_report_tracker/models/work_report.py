# -*- coding: utf-8 -*-

from odoo import fields, models, api,_
from odoo.tools import email_normalize
from bs4 import BeautifulSoup
from datetime import datetime



class WorkReport(models.Model):
    """work Report"""
    _name = 'work.report'
    _inherit = 'mail.thread.blacklist'
    _primary_email = 'email_from'
    _description = 'Work Report'

    subject = fields.Char(required=True)
    email_from = fields.Char(required=True)
    name = fields.Many2one('hr.employee',string="Employee")
    body = fields.Html('body')
    date = fields.Date(string='Date')
    work_ids = fields.One2many('work.report.lines', 'report_id', string="Works")


    @api.model
    def message_new(self, msg_dict, custom_values=None):
        """create new work report record from email"""
        print("msg_dict",msg_dict)

        email_address = email_normalize(msg_dict.get('email_from'))
        print(email_address)



        # if custom_values is None:
        #     custom_values = {}

        html_body = msg_dict.get('body')
        soup = BeautifulSoup(html_body, 'html.parser')
        print('soup',soup)

        rows = soup.find_all('tr')
        print("rows",rows)

        lines = []
        for row in rows[2:]:
            data = [td.get_text(strip=True) for td in row.find_all('td')]
            print('values',data)
            print('values[0]',data[1])
            pro_name = data[1]
            task = data[2]
            remarks = data[4]

            print('pro_name', pro_name)
            print('remarks', remarks)

            existing_project = self.env['project.project'].search([('name','=',pro_name)])
            if not existing_project:
                new_proj = self.env['project.project'].create({
                    'name': pro_name,
                })
            pro_id = self.env['project.project'].search([('name','=',pro_name)])

            report = self.env['work.report.lines'].create({
                'project_id': pro_id.id,
                'remarks': remarks,
                'task': task,
            })


            print('p',report)
            print('k',report.id)

            lines.append(report.id)
            print('new_lines',lines)

            sub = msg_dict.get('subject')
            split = sub.split('_',2)
            print('split',split)
            report_date = split[1]

            lower_name = split[2].lower()
            print('employee_name',lower_name)
            result = lower_name.replace("_", " ").title()
            print('result',result)

            employee = self.env['hr.employee'].search([
                ('name', '=', result)
            ], limit=1)

            date_obj = datetime.strptime(report_date, "%d %b %Y")
            formatted_date = date_obj.strftime("%Y-%m-%d")

        defaults = {
            'subject': msg_dict.get('subject') or _("No Subject"),
            'email_from': email_address,
            'name': employee.id if employee else None,
            'date': formatted_date,
            'body': msg_dict.get('body'),
            'work_ids': [fields.Command.set(lines)]
        }

        new_report = super().message_new(msg_dict, custom_values=defaults)
        # new_lead._assign_userless_lead_in_team(_('incoming email'))
        return new_report





