# -*- coding: utf-8 -*-

{
    'name': 'Work Report Tracker',
    'version': '19.0.1.0.0',
    'licence': 'LGPL-3',
    'summary': """Work Report Tracker""",
    'description': """Work Report Tracker""",
    'sequence': -10,
    'category': 'work report',
    'installable': True,
    'application': True,
    'depends': ['base','hr'],
    'data': [
        'security/ir.model.access.csv',
        'views/work_report_views.xml',
        'views/work_report_menus.xml'

        # 'security/ir.model.access.csv',
        # "views/product_template_views.xml",
        # "views/badge_template_views.xml"
    ]
}
