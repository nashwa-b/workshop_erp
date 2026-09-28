# -*- coding: utf-8 -*-

from odoo import api, models

import io
import xlsxwriter
import datetime
from odoo.http import Controller, request, route, content_disposition


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

        params = []
        if docs.start_date:
            query += """AND job_date >= %s"""
            params.append(docs.start_date)

        if docs.end_date:
            query += """ AND job_date <= %s """
            params.append(docs.end_date)

        if docs.vehicle_id:
            query += """AND jo.vehicle_id = %s"""
            params.append(docs.vehicle_id.id)

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
        domain = []
        if data.get('start_date'):
            domain.append(('job_date','>=',data.get('start_date')))

        if data.get('end_date'):
            domain.append(('job_date','<=',data.get('end_date')))

        if data.get('customer_id'):
            domain.append(('customer_id','=',data.get('customer_id')))

        if data.get('vehicle_id'):
            domain.append(('vehicle_id','=',data.get('vehicle_id')))

        job_orders = self.env['workshop.job.order'].search(domain)
        print(job_orders)

        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet('Job Orders')

        sheet.set_column(0,0, 20)
        sheet.set_column(1,1, 20)
        sheet.set_column(2,2, 20)
        sheet.set_column(3,3, 20)
        sheet.set_column(4,4, 20)
        sheet.set_column(5,5, 20)
        sheet.set_column(6,6, 20)
        sheet.set_column(7,7, 20)
        sheet.set_column(8,8, 20)
        sheet.set_column(9,9, 20)
        sheet.set_column(10,10, 20)

        head = workbook.add_format(
            {'bold': True, 'font_size': 30, 'align': 'center'})
        field_head = workbook.add_format(
            {'bold': True,  'align': 'center','border':1})
        sub_heading = workbook.add_format(
            { 'bold': True, 'align': 'center'})
        date_format = workbook.add_format({'text_wrap': True, 'num_format': 'dd-mm-yyyy'})
        sheet.merge_range('C3:K6', 'Job Orders', head)


        row = 23
        heading_row = 22
        line_row = 27
        i=0
        for job_order in job_orders:

            row += 1
            i+=1
            status = dict(self.env['workshop.job.order']._fields['status'].selection).get(job_order.status)
            company_ids = self.env.get('job_order.company_id')
            print('u',company_ids)

            if data.get('customer_id'):
                sheet.write(10,0 ,'Customer:',sub_heading)
                sheet.write(10,1, job_order.customer_id.name)

            if data.get('vehicle_id'):
                sheet.write(11,0,'Vehicle',sub_heading)
                sheet.write(11,1,job_order.vehicle_id.name)

            if data.get('start_date'):
                sheet.write(12,0, 'Start Date:',sub_heading)
                sheet.write(12,1, data.get('start_date'))
            if data.get('end_date'):
                sheet.write(13,0, 'End Date:',sub_heading)
                sheet.write(13,1, data.get('end_date'))

            sheet.write(0,0,job_order.company_id.name)
            if job_order.company_id.partner_id.street:
                sheet.write(1,0,job_order.company_id.partner_id.street)
            if job_order.company_id.partner_id.city:
                sheet.write(2,0,job_order.company_id.partner_id.city)
            if job_order.company_id.partner_id.zip:
                sheet.write(3,0,job_order.company_id.partner_id.zip)
            if job_order.company_id.partner_id.country_id:
                sheet.write(3,0,job_order.company_id.partner_id.country_id.name)

            sheet.write(heading_row,0,job_order.name,sub_heading)

            heading_row+=11
            sheet.write(row,0 , 'Sl No',field_head)
            sheet.write(row, 1, 'Job Date',field_head)
            sheet.write(row, 2, 'Customer',field_head)
            sheet.write(row, 3, 'Vehicle',field_head)
            sheet.write(row, 4, 'Total',field_head)
            sheet.write(row, 5, 'Status',field_head)

            if data.get('detailed_view'):
                sheet.write(row, 6, 'Warranty',field_head)
                sheet.write(row, 7, 'Collected',field_head)
                sheet.write(row, 8, 'Company',field_head)
                sheet.write(row, 9, 'Sale Order No',field_head)
                sheet.write(row, 10, 'Invoice NO',field_head)

            row+=1
            sheet.write(row, 0, i)
            sheet.write(row, 1, job_order.job_date,date_format)
            print(job_order.job_date)
            sheet.write(row, 2, job_order.customer_id.name)
            sheet.write(row, 3, job_order.vehicle_id.name)
            sheet.write(row, 4, job_order.total)
            sheet.write(row, 5, status)

            if data.get('detailed_view'):
                sheet.write(row, 6, job_order.warranty)
                sheet.write(row, 7, job_order.collected)
                sheet.write(row, 8, job_order.company_id.name)
                sheet.write(row, 9, job_order.sale_order_id.name)
                sheet.write(row, 10, job_order.invoice_id.name)

            row+=4
            sheet.write(line_row,1,'Job Lines', sub_heading)
            line_row+=11

            if data.get('detailed_view'):
                sheet.write(row, 1, 'product',field_head)
                sheet.write(row, 2, 'Quantity',field_head)
                sheet.write(row, 3, 'Unit Price',field_head)
                sheet.write(row, 4, 'Total',field_head)

                row+=1
                for order_line in job_order.order_line_ids:
                    sheet.write(row, 1, order_line.product_id.name)
                    sheet.write(row, 2, order_line.product_qty)
                    sheet.write(row, 3, order_line.price_unit)
                    sheet.write(row, 4, order_line.sub_total)
                row+=1
            row+=3

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()