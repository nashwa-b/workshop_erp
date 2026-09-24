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
        query = """select jol.product_id as product,jol.product_qty as quantity, jol.price_unit as unit_price, jol.sub_total as total,jo.warranty as warranty, jo.collected as collected,rc.name as company,so.name as sale,iv.name as invoice,jo.name as name,wv.name->>'en_US' as vehicle,wb.name->>'en_US' as bay,pr.name as customer,jo.job_date as job_date,jo.total as total,jo.status as status from workshop_job_order as jo
                               left join res_partner as pr on pr.id = jo.customer_id
                               left join workshop_job_line as jol on jol.order_id = jo.id
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
            'data': data,

        }

    # def action_print_xlsx(self):
    #     """
    #     Returns report action for the XLSX Attendance report
    #     Raises: ValidationError: if From Date > To Date
    #     Raises: ValidationError: if there is no attendance records
    #     Returns:
    #         dict:  the XLSX report action
    #     """
    #     if not self.from_date:
    #         self.from_date = date.today()
    #     if not self.to_date:
    #         self.to_date = date.today()
    #     if self.from_date > self.to_date:
    #         raise ValidationError(_('From Date must be earlier than To Date.'))
    #     attendances = self.env['hr.attendance'].search(
    #         [('employee_id', 'in', self.employee_ids.ids)])
    #     data = {
    #         'from_date': self.from_date,
    #         'to_date': self.to_date,
    #         'employee_ids': self.employee_ids.ids
    #     }
    #     if self.employee_ids and not attendances:
    #         raise ValidationError(
    #             _("There is no attendance records for the employee"))
    #     if self.from_date and self.to_date:
    #         return {
    #             'type': 'ir.actions.report',
    #             'data': {'model': 'employee.attendance.report',
    #                      'options': json.dumps(data, default=json_default),
    #                      'output_format': 'xlsx',
    #                      'report_name': 'Attendance Report',
    #                      },
    #             'report_type': 'xlsx',
    #         }

        # def get_xlsx_report(self, data, response):
        #     """
        #     Print the XLSX report
        #     Returns: None
        #     """
        #     query = """select hr_e.name,date(hr_at.check_in),
        #            SUM(hr_at.worked_hours) from hr_attendance hr_at LEFT JOIN
        #            hr_employee hr_e ON hr_at.employee_id = hr_e.id"""
        #     if not data['employee_ids']:
        #         query += """ GROUP BY date(check_in), hr_e.name"""
        #     else:
        #         query += """ WHERE hr_e.id in (%s) GROUP BY date(check_in),
        #            hr_e.name""" % (', '.join(str(employee_id)
        #                                      for employee_id in data['employee_ids']))
        #     self.env.cr.execute(query)
        #     docs = self.env.cr.dictfetchall()
        #     output = io.BytesIO()
        #     workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        #     sheet = workbook.add_worksheet('docs')
        #     start_date = datetime.strptime(data['from_date'], '%Y-%m-%d').date()
        #     end_date = datetime.strptime(data['to_date'], '%Y-%m-%d').date()
        #     date_range = rrule(DAILY, dtstart=start_date, until=end_date)
        #     sheet.set_column(1, 1, 15)
        #     sheet.set_column(2, 2, 15)
        #     border = workbook.add_format({'border': 1})
        #     green = workbook.add_format({'bg_color': '#28A828', 'border': 1})
        #     red = workbook.add_format({'bg_color': '#ff3333', 'border': 1})
        #     rose = workbook.add_format({'bg_color': '#DA70D6', 'border': 1})
        #     head = workbook.add_format(
        #         {'bold': True, 'font_size': 30, 'align': 'center'})
        #     date_size = workbook.add_format(
        #         {'font_size': 12, 'bold': True, 'align': 'center'})
        #     sheet.merge_range('C3:K6', 'Attendance Report', head)
        #     sheet.merge_range('B8:C9', 'From Date: ' + data['from_date'], date_size)
        #     sheet.merge_range('B10:C11', 'To Date: ' + data['to_date'], date_size)
        #     sheet.write(2, 12, '', green)
        #     sheet.write(2, 13, 'Present')
        #     sheet.write(4, 12, '', red)
        #     sheet.write(4, 13, 'Absent')
        #     sheet.write(6, 12, '', rose)
        #     sheet.write(6, 13, 'Half Day')
        #     sheet.merge_range('B16:B17', 'Sl.No', border)
        #     sheet.merge_range('C16:C17', 'Employee', border)
        #     row = 15
        #     col = 2
        #     for date_data in date_range:
        #         col += 1
        #         sheet.write(row, col, date_data.strftime('%Y-%m-%d'), border)
        #     row = 16
        #     col = 2
        #     for date_data in date_range:
        #         col += 1
        #         sheet.write(row, col, date_data.strftime('%a'), border)
        #     employee_names = []
        #     attendance_list = []
        #     for doc in docs:
        #         if doc['name'] not in employee_names:
        #             date_sum_list = []
        #             employee_names.append(doc['name'])
        #             for date_data in date_range:
        #                 date_out = date_data.strftime('%Y-%m-%d')
        #                 record_list = list(
        #                     filter(
        #                         lambda x: x['name'] == doc['name'] and x[
        #                             'date'].strftime(
        #                             '%Y-%m-%d') == date_out, docs))
        #                 if record_list:
        #                     date_sum_list.append(record_list[0])
        #                 else:
        #                     date_sum_list.append({
        #                         'name': '',
        #                         'date': '',
        #                         'sum': 0
        #                     })
        #             attendance_list.append(
        #                 {'name': doc['name'], 'items': date_sum_list})
        #     work = self.env.ref('resource.resource_calendar_std')
        #     row = 17
        #     i = 0
        #     for rec in attendance_list:
        #         row += 1
        #         col = 1
        #         i += 1
        #         sheet.write(row, col, i, border)
        #         col += 1
        #         sheet.write(row, col, rec['name'], border)
        #         for item in rec['items']:
        #             col += 1
        #             if item['sum'] >= work.hours_per_day:
        #                 sheet.write(row, col, item['sum'], green)
        #             elif 1 <= item['sum'] <= 4 or 4 <= item['sum'] <= \
        #                     work.hours_per_day:
        #                 sheet.write(row, col, item['sum'], rose)
        #             else:
        #                 sheet.write(row, col, item['sum'], red)
        #     workbook.close()
        #     output.seek(0)
        #     response.stream.write(output.read())
        #     output.close()