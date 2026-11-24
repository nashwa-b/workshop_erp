# -*- coding: utf-8 -*-

from odoo import api, models


class WorkReportHistory(models.AbstractModel):
    _name = 'report.work_report_tracker.report_work_report'
    _description = "Work Report History"

    @api.model
    def _get_report_values(self, docids, data = None):
        """Print the PDF report of work report"""
        docs = self.env['work.report.wizard'].browse(docids)
        print('o',docs)
        query = """select wr.id as work_report_id,wr.date as date,wr.name as name, pr.name as employee,  wrl.remarks as remarks from work_report as wr
                               left join hr_employee as pr on pr.id = wr.name
                               left join  work_report_lines as wrl on wrl.report_id = wr.id
                                where 1=1"""

        params = []
        if docs.start_date:
            query += """ AND date >= %s"""
            params.append(docs.start_date)

        if docs.end_date:
            query += """ AND date <= %s """
            params.append(docs.end_date)

        if docs.employee_id:
            query += """ AND wr.name = %s"""
            params.append(docs.employee_id.id)

        if docs.project_id:
            query += """ AND wrl.project_id = %s"""
            params.append(docs.project_id.id)

        self.env.cr.execute(query, params)
        report = self.env.cr.dictfetchall()

        print('p',report)
        data = {
            'report':report
        }
        print(docs)
        return {
            'doc_ids': docids,
            'doc_model': 'work.report.wizard',
            'docs': docs,
            'data': data
        }