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
    'depends': ['base', 'hr', 'web', 'sale', 'account', 'product', 'website_sale', 'mail', 'contacts', 'calendar',
                'website','point_of_sale'],
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
        "report/workshop_job_order_report_template.xml",
        "report/workshop_job_order_report_views.xml",
        "wizard/workshop_job_order_history_wizard_views.xml",
        "views/job_order_website_template.xml",
        "views/job_order_form_template.xml",
        "views/job_order_submit_template.xml",
        "views/appointment_template.xml",
        "views/job_order_view_template.xml",
        "views/snippets/vehicle_template.xml",
        "views/vehicle_view_template.xml",
        "views/res_config_settings.xml",
        "views/pos_category_views.xml",
        "views/website_menus.xml",
        "views/workshop_erp_menus.xml",

    ],
    'assets': {
        'web.assets_backend': [
            '/workshop_erp/static/src/js/report_xlsx.js'],

        'web.assets_frontend': [
            '/workshop_erp/static/src/js/job_lines.js',
                                '/workshop_erp/static/src/js/top_vehicles.js',
                                '/workshop_erp/static/src/xml/top_vehicles_template.xml'
                                ],

        'web.assets_unit_tests': [
            '/workshop_erp/static/tests/pos_category.data.js',
        ],

        'point_of_sale._assets_pos': [
            '/workshop_erp/static/src/js/order_display.js',
            '/workshop_erp/static/src/js/order_line.js',
            # '/workshop_erp/static/src/js/pos_order_line.js',
            # '/workshop_erp/static/src/js/discount_validation.js',
            '/workshop_erp/static/src/xml/pos_spare_type.xml',
            '/workshop_erp/static/src/css/pos_spare_type.css',
            '/workshop_erp/static/src/xml/pos_order_line_views.xml'
        ],

    },

}
