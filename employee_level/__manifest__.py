# -*- coding: utf-8 -*-

{
    'name': 'Employee Level',
    'version': '19.0.1.0.0',
    'licence': 'LGPL-3',
    'summary': """Employee Level""",
    'description': """Employee Level""",
    'sequence': -10,
    'category': 'employee level',
    'application': True,
    'installable': True,
    'depends': ['base','hr'],
    'data': ["security/ir.model.access.csv",
        "views/employee_level_views.xml", "views/hr_employee_views.xml"
        ]
}