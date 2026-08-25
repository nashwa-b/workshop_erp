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
    'depends': ['base', 'hr','sale'],
    'data': [
        "security/ir.model.access.csv",
        "data/sequence_data.xml",
        "data/workshop_bay_data.xml",
        "views/workshop_bay_views.xml",
        "views/workshop_vehicle_views.xml",
        "views/workshop_job_order_views.xml",
        "views/workshop_job_line_views.xml",
        "views/res_partner_views.xml",
        "views/sale_order_views.xml",
        "views/workshop_erp_menus.xml"
    ]
}
