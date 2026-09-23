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
        # ledger_view = self.env['export.general.ledger.view'].browse(self._context.get('active_ids', []))

        # report = self.env.cr.dictfetchall()
        # data = {'form':self.read(['customer_id', 'vehicle_id','start_date','end_date'])}

        data = {
            'model_id': self.id,
            'end_date': self.end_date,
            'from_date': self.start_date,
            'vehicle_name': self.vehicle_id,
            'customer_id': self.customer_id
        }
        # return self.env.ref('my_module.action_my_custom_report').with_context(
        #     wizard_data=data
        # ).report_action(self)
        docids = self.env['workshop.job.order'].search([]).ids
        return self.env.ref('workshop_erp.action_report_joborder').with_context(
            wizard_data=data).report_action(None, docids, data)

        # data = {'form':self.read(['customer_id', 'vehicle_id','start_date','end_date'])[0]}
        #     # 'customer': self.customer_id.id if self.customer_id else None,
        #     #     'vehicle': self.vehicle_id.id if self.vehicle_id else None,
        #     #     'start_date': self.start_date,
        #     #     'end_date': self.end_date}
        # print(data)
        # return self.env.ref("workshop_erp.action_report_joborder").report_action(self.ids,data = data)

    # data = {
    #     'form': self.read(['date_from', 'date_to'])[0]
    # }

    # form_data = data.get('form', {})
    # date_from = form_data.get('date_from')
    # date_to = form_data.get('date_to')



