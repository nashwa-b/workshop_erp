# -*- coding: utf-8 -*-

{
    'name': 'Employee Loan Management',
    'version': '19.0.1.0.0',
    'licence': 'LGPL-3',
    'summary': """Employee Loan Management""",
    'description': """Employee Loan Management""",
    'sequence': 1,
    'category': 'Employee Loan',
    'application': True,
    'installable': True,
    'depends': ['hr'],
    'data': [
        "security/ir.model.access.csv",
        "data/sequence_data.xml",
        "views/hr_employee_views.xml",
        "views/employee_loan_menus.xml",
        "views/employee_loan_views.xml"
      ]
}

