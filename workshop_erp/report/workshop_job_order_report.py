# -*- coding: utf-8 -*-

from odoo import api, fields, models

# from odoo.addons.sale.models.sale_order import SALE_ORDER_STATE

class WorkshopErpReport(models.AbstractModel):
    _name = 'report.workshop_erp.report_job_orders'
    _description = "Job Order History Report"
    # customer_id = fields.Many2one('res.partner', string="Customer")
    # vehicle_id = fields.Many2one('workshop.vehicle', string="Vehicle")
    # start_date = fields.Date(string="Start Date")
    # end_date = fields.Date(string="End Date")
    # _auto = False
    # _rec_name = 'date'
    # _order = 'date desc'

    @api.model
    def _get_report_values(self, docids, data=None):
        # form_data = data.get('form', {})
        # start_date = form_data.get('start_date')
        # # print('l',self.start_date)
        # end_date = form_data.get('end_date')
        # vehicle_id = form_data.get('vehicle_id')
        # customer_id = form_data.get('customer_id')

        wizard_context_data = self.env.context.get('wizard_data', {})
        start_date = wizard_context_data.get('start_date')
        end_date = wizard_context_data.get('end_date')
        vehicle_id = wizard_context_data.get('vehicle_id')
        customer_id = wizard_context_data.get('customer_id')

        # Method 2: Browsing the wizard directly using docids
        # (Best practice if you need to fetch many fields from the wizard)
        wizard_record = self.env['my.report.wizard'].browse(docids)

        query = """select jo.name as name,wv.name as vehicle,wb.name as bay,pr.name as customer,jo.job_date as job_date,jo.total as total,jo.status as status from workshop_job_order as jo
                               left join res_partner as pr on pr.id = jo.customer_id
                               left join workshop_vehicle as wv on wv.id = jo.vehicle_id
                                left join workshop_bay as wb on wb.id = jo.bay_id where 1= 1"""

        # query = """select jo.name,wv.name,jo.job_date,jo.total,jo.status from workshop_job_order as jo
        #              inner join workshop_vehicle as wv on wv.id = jo.vehicle_id
        #              where 1=1"""
        params = []
        if start_date:
            # query += """ where tb.date >= '%s' and tb.date <= '%s'""" % self.from_date, %self.to_date

            # query += """ AND jo.job_date >= '%s' and jo.job_date <= '%s'""" % self.start_date, %self.end_date
            query += """AND job_date >= %s"""
            params.append(start_date)
            # param.append(self.end_date)
        if end_date:
            # query += """ where tb.date >= '%s' and tb.date <= '%s'""" % self.from_date, %self.to_date

            # query += """ AND jo.job_date >= '%s' and jo.job_date <= '%s'""" % self.start_date, %self.end_date
            query += """ AND job_date <= %s """
            # param.append(self.start_date)
            params.append(end_date)
        if vehicle_id:
            query += """AND jo.vehicle_id = %s"""
            params.append(vehicle_id.id)
            # param.append(self.vehicle_id.id)
        if customer_id:
            query += """AND jo.customer_id = %s"""
            params.append(customer_id.id)

        self.env.cr.execute(query, params, [start_date, end_date, vehicle_id, customer_id])
        report = self.env.cr.dictfetchall()
        print(report)

        # report = self.env['ir.actions.report']._get_report_from_name('module.report_name')
        # # get the records selected for this rendering of the report
        # obj = self.env[report.model].browse(docids)
        # # return a custom rendering context
        # return {
        #     'lines': docids.get_lines()
        # }


        # print('l',docs)
        # print('o',data['report'])
        docs = self.env['workshop.job.order.wizard'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'workshop.job.order.wizard',
            'docs': docs,
            'data': data,
            'report': report,
        }

        return {
            'doc_ids': docids,
            'doc_model': 'workshop.job.order.wizard',
            'docs':docs ,
            'data': data,
            'customer_id':customer_id,
            'vehicle_id':vehicle_id,
            'start_date':start_date,
            'end_date':end_date,
            # 'report': report,
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