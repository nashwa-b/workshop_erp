# -*- coding: utf-8 -*-

{
    'name': 'Fleet Service',
    'version': '19.0.1.0.0',
    'licence': 'LGPL-3',
    'summary': """Fleet service""",
    'description': """Fleet service""",
    'sequence': 1,
    'category': 'Fleet Service',
    'application': True,
    'installable': True,
    'depends': ['base','fleet','hr','product'],
    'data': [
        "security/ir.model.access.csv",
        "data/sequence_data.xml",
        "data/type.xml",
        "views/fleet_service_order.xml",
        "views/fleet_service_menus.xml",
        # "security/ir.model.access.csv",
        # "data/sequence_data.xml",
        # "views/hr_employee_views.xml",
        # "views/employee_loan_menus.xml",
        # "views/employee_loan_views.xml"
      ]
}