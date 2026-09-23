# -*- coding: utf-8 -*-

from odoo import api, fields, models

# from odoo.addons.sale.models.sale_order import SALE_ORDER_STATE

class WorkshopErpReport(models.AbstractModel):
    _name = 'report.workshop_erp.report_job_orders'
    _description = "Job Order History Report"
    # _rec_name = 'date'
    # _order = 'date desc'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['workshop.job.order.wizard'].browse(docids)
        print('o',docs)


        query = """select jo.name as name,wv.name as vehicle,wb.name as bay,pr.name as customer,jo.job_date as job_date,jo.total as total,jo.status as status from workshop_job_order as jo
                               left join res_partner as pr on pr.id = jo.customer_id
                               left join workshop_vehicle as wv on wv.id = jo.vehicle_id
                                left join workshop_bay as wb on wb.id = jo.bay_id where 1=1 """

        params = []
        if docs.start_date:
            # query += """ where tb.date >= '%s' and tb.date <= '%s'""" % self.from_date, %self.to_date

            # query += """ AND jo.job_date >= '%s' and jo.job_date <= '%s'""" % self.start_date, %self.end_date
            query += """AND job_date >= %s"""
            params.append(docs.start_date)
            # param.append(self.end_date)
        if docs.end_date:
            # query += """ where tb.date >= '%s' and tb.date <= '%s'""" % self.from_date, %self.to_date

            # query += """ AND jo.job_date >= '%s' and jo.job_date <= '%s'""" % self.start_date, %self.end_date
            query += """ AND job_date <= %s """
            # param.append(self.start_date)
            params.append(docs.end_date)
        if docs.vehicle_id:
            query += """AND jo.vehicle_id = %s"""
            params.append(docs.vehicle_id.id)
            # param.append(self.vehicle_id.id)
        if docs.customer_id:
            query += """AND jo.customer_id = %s"""
            params.append(docs.customer_id.id)

        self.env.cr.execute(query, params)
        report = self.env.cr.dictfetchall()
        print('p',report)

        data = {
            'report':report
        }

        # docs = self.env['workshop.job.order.wizard'].browse(docids)

        print(docs)

        return {
            'doc_ids': docids,
            'doc_model': 'workshop.job.order.wizard',
            'docs': docs,
            'data': data,
        }

       


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