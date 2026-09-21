# -*- coding: utf-8 -*-

{
    'name': 'Employee Transfer',
    'version': '19.0.1.0.0',
    'licence': 'LGPL-3',
    'summary': """Employee Transfer Request""",
    'description': """Employee Transfer""",
    'sequence': 1,
    'category': 'Employee Transfer',
    # 'application': True,
    'installable': True,
    'depends': ['base','hr'],
    'data': [
        "security/ir.model.access.csv",
        "wizard/employee_transfer_wizard_views.xml",
        "views/res_users_views.xml",
        "views/employee_transfer_request_views.xml",
    ]
}