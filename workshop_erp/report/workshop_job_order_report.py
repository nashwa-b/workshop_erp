# -*- coding: utf-8 -*-

from odoo import api, fields, models

import io
import json
from datetime import datetime, date
from dateutil.rrule import rrule, DAILY
from odoo.exceptions import ValidationError
from odoo.tools import date_utils, json_default
import xlsxwriter


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
        query = """select jo.id as job_order_id,jo.warranty as warranty, jo.collected as collected,rc.name as company,so.name as sale,iv.name as invoice,jo.name as name,wv.name->>'en_US' as vehicle,wb.name->>'en_US' as bay,pr.name as customer,jo.job_date as job_date,jo.total as total,jo.status as status from workshop_job_order as jo
                               left join res_partner as pr on pr.id = jo.customer_id
                               left join res_company as rc on rc.id = jo.company_id
                               left join sale_order as so on so.id = jo.sale_order_id
                               left join account_move as iv on iv.id = jo.invoice_id
                               left join workshop_vehicle as wv on wv.id = jo.vehicle_id
                                left join workshop_bay as wb on wb.id = jo.bay_id where 1=1"""
        # queryy="""select  jo.warranty, jo.collected,jo.company_id,jo.order_line_ids from workshop_job_order as jo where 1=1"""
        # orders = self.env['workshop_job_order'].browse(docids)

        params = []
        if docs.start_date:
            query += """AND job_date >= %s"""
            params.append(docs.start_date)
            # param.append(self.end_date)

        if docs.end_date:
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


        status_selection = dict(self.env['workshop.job.order']._fields['status'].selection)
        for line in report:
            line['status'] = status_selection.get(line['status'],line['status'])
        print('p',report)

        data = {
            'report':report
        }
        print(docs)
        return {
            'doc_ids': docids,
            'doc_model': 'workshop.job.order.wizard',
            'docs': docs,
            'data': data
        }

    def get_xlsx_report(self, data, response):
        print('l',self)
        """
        Print the XLSX report
        Returns: None
        """
        query = """select jo.id as job_order_id,jo.warranty as warranty, jo.collected as collected,rc.name as company,so.name as sale,iv.name as invoice,jo.name as name,wv.name->>'en_US' as vehicle,wb.name->>'en_US' as bay,pr.name as customer,jo.job_date as job_date,jo.total as total,jo.status as status from workshop_job_order as jo
                                     left join res_partner as pr on pr.id = jo.customer_id
                                     left join res_company as rc on rc.id = jo.company_id
                                     left join sale_order as so on so.id = jo.sale_order_id
                                     left join account_move as iv on iv.id = jo.invoice_id
                                     left join workshop_vehicle as wv on wv.id = jo.vehicle_id
                                      left join workshop_bay as wb on wb.id = jo.bay_id where 1=1"""

        params = []
        if data.start_date:
            query += """AND job_date >= %s"""
            params.append(data.start_date)
            # param.append(self.end_date)
            print(query)

        if data.end_date:
            query += """ AND job_date <= %s """
            params.append(data.end_date)

        if data.vehicle_id:
            query += """AND jo.vehicle_id = %s"""
            params.append(data.vehicle_id.id)

        if data.customer_id:
            query += """AND jo.customer_id = %s"""
            params.append(data.customer_id.id)
        self.env.cr.execute(query,params)
        print(query)
        docs = self.env.cr.dictfetchall()
        print('d',docs)
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet('docs')
        sheet.set_column(1, 1, 15)
        sheet.set_column(2, 2, 15)

        head = workbook.add_format(
            {'bold': True, 'font_size': 30, 'align': 'center'})
        date_size = workbook.add_format(
            {'font_size': 12, 'bold': True, 'align': 'center'})
        sheet.merge_range('C3:K6', 'Job Orders', head)
        sheet.merge_range('B8:C9', 'From Date: ' + data['start_date'], date_size)
        sheet.merge_range('B10:C11', 'To Date: ' + data['end_date'], date_size)
        sheet.set_column('C:C',20)
        sheet.set_column('D:D',20)
        sheet.set_column('E:E',20)
        sheet.set_column('F:F',20)
        sheet.set_column('G:G',20)
        sheet.set_column('H:H',20)
        row=5
        col=2
        sheet.write(row, col, 'Job Date', head)
        sheet.write(row, col+1, 'Vehicle',head)
        sheet.write(row, col+2, 'Total', head)
        sheet.write(row, col+3, 'Status',head)
        sheet.write(row, col+4, 'Warranty', head)
        sheet.write(row, col+5, 'Collected',head)
        sheet.write(row, col+6, 'Company',head)

        row+=1
        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()