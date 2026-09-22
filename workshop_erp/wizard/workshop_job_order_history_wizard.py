# -*- coding: utf-8 -*-

from odoo import fields, models


class WorkshopJobOrderHistoryWizard(models.TransientModel):
    """Creation of Wizard for employee transfer"""
    _name = 'workshop.job.order.wizard'
    _description = 'Job Order History'

    customer_id = fields.Many2one('res.partner', string="Customer")
    vehicle_id = fields.Many2one('workshop.vehicle', string="Vehicle")
    start_date = fields.Datetime(string="Start Date")
    end_date = fields.Datetime(string="End Date")

    def action_report_job_order(self):
            query = """select jo.name,wv.name as vehicle,pr.name as customer,jo.job_date,jo.bay_id,jo.total,jo.status,jol.product_id from workshop_job_order as jo
                       left join res_partner as pr on pr.id = jo.customer_id
                       left join workshop_vehicle as wv on wv.id = jo.vehicle_id
                        left join workshop_job_line as jol on jol.order_id = jo.id where 1= 1"""

            # query = """select jo.name,wv.name,jo.job_date,jo.total,jo.status from workshop_job_order as jo
            #              inner join workshop_vehicle as wv on wv.id = jo.vehicle_id
            #              where 1=1"""
            param = []
            if self.start_date:
                # query += """ where tb.date >= '%s' and tb.date <= '%s'""" % self.from_date, %self.to_date

                # query += """ AND jo.job_date >= '%s' and jo.job_date <= '%s'""" % self.start_date, %self.end_date
                query += """ And jo.job_date >= %s and jo.job_date <= %s"""
                param.append(self.start_date)
                param.append(self.end_date)
            if self.vehicle_id:
                query += """ And jo.vehicle_id = '%s'""" % self.vehicle_id.id
                # param.append(self.vehicle_id.id)
            if self.customer_id:
                query += """ And jo.customer_id = '%s'""" % self.customer_id.id

            self.env.cr.execute(query,param)
            report = self.env.cr.dictfetchall()
            print(report)
            data = {'customer_id': self.customer_id.id,
                    'vehicle_id': self.vehicle_id.id,
                    'start_date': self.start_date,
                    'end_date': self.end_date,
                    'report': report
                    }
            return self.env.ref(
                "workshop_erp.action_report_joborder"
            ).report_action(self)

