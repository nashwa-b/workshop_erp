# -*- coding: utf-8 -*-

{
    'name': 'Workshop',
    'version': '19.0.1.0.0',
    'licence': 'LGPL-3',
    'summary': """A Workshop ERP System""",
    'description': """Workshop ERP System""",
    'sequence': -10,
    'category': 'Workshop',
    'application': True,
    'installable': True,
    'depends': ['base', 'hr','sale','account','product','website_sale','mail','contacts','calendar'],
    'data': [
        "security/workshop_erp_groups.xml",
        "security/workshop_job_order_security.xml",
        "security/ir.model.access.csv",
        "data/ir_cron_data.xml",
        "data/mail_template_data.xml",
        "data/sequence_data.xml",
        "data/workshop.bay.csv",
        "data/job_type_data.xml",
        "data/workshop_bay_data.xml",
        "views/workshop_job_order_views.xml",
        "views/workshop_vehicle_views.xml",
        "views/job_type_views.xml",
        "views/hr_employee_views.xml",
        "views/workshop_bay_views.xml",
        "views/res_partner_views.xml",
        "views/sale_order_views.xml",
        "views/workshop_job_order_reporting_views.xml",
        "views/calendar_event_views.xml",
        "wizard/workshop_job_order_history_wizard_views.xml",
        "report/workshop_job_order_report_views.xml",
        "report/workshop_job_order_report_template.xml",
        "views/workshop_erp_menus.xml"
    ]
}
