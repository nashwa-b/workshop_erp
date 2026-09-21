# -*- coding: utf-8 -*-

from odoo import api, fields, models

# from odoo.addons.sale.models.sale_order import SALE_ORDER_STATE

class WorkshopErpReport(models.Model):
    _name = 'workshop_erp.report'
    _description = "Job Order Analysis Report"
    _auto = False
    _rec_name = 'date'
    _order = 'date desc'

    start_date = fields.Datetime(string="Start Date")
    end_date = fields.Datetime(string="End Date")

    # def action_report_job_order(self):
    #     pass
        # query = """select pr.name,fv.name as truck,gt.name as goods,tb.from_location,tb.to_location,tb.distance,
        #            tb.weight,tb.unit,amount,tb.date,tb.state from truck_booking as tb
        #            inner join res_partner as pr on pr.id = tb.partner_id
        #            inner join fleet_vehicle_model as fv on fv.id = tb.truck_id
        #            inner join goods_type as gt on gt.id = tb.goods_type_id """
        # if self.from_date:
        #     query += """ where tb.date >= '%s' and tb.date <= '%s'""" % self.from_date, %self.to_date
        # self.env.cr.execute(query)
        # report = self.env.cr.dictfetchall()
        # data = {'date': self.read()[0], 'report': report}
        # return self.env.ref('module_name.action_report_booking').report_action(None, data=data)