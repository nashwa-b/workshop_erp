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
            query = """select pr.name,fv.name as truck,gt.name as goods,tb.from_location,tb.to_location,tb.distance,
                       tb.weight,tb.unit,amount,tb.date,tb.state from workshop_job_order as tb
                       inner join res_partner as pr on pr.id = tb.partner_id
                       inner join fleet_vehicle_model as fv on fv.id = tb.truck_id
                       inner join goods_type as gt on gt.id = tb.goods_type_id """
            if self.from_date:
                query += """ where tb.job_date >= '%s' and tb.job_date <= '%s'""" % self.start_date_date, %self.end_date
            self.env.cr.execute(query)
            report = self.env.cr.dictfetchall()
            data = {'date': self.read()[0], 'report': report}
            return self.env.ref(
                "workshop_erp.action_report_joborder"
            ).report_action(self)

    # def action_report_job_order(self):
    #     pass
    #     query = """select pr.name,fv.name as truck,gt.name as goods,tb.from_location,tb.to_location,tb.distance,
    #                tb.weight,tb.unit,amount,tb.date,tb.state from truck_booking as tb
    #                inner join res_partner as pr on pr.id = tb.partner_id
    #                inner join fleet_vehicle_model as fv on fv.id = tb.truck_id
    #                inner join goods_type as gt on gt.id = tb.goods_type_id """
    #     if self.from_date:
    #         query += """ where tb.date >= '%s' and tb.date <= '%s'""" % self.start_date_date, %self.end_date
    #     self.env.cr.execute(query)
    #     report = self.env.cr.dictfetchall()
    #     data = {'date': self.read()[0], 'report': report}
    #     return self.env.ref('module_name.action_report_booking').report_action(None, data=data)
    #
    #
    #
