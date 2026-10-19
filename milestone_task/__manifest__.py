# -*- coding: utf-8 -*-

{
    'name': 'Milestone Task',
    'version': '19.0.1.0.0',
    'licence': 'LGPL-3',
    'summary': """Milestone Task""",
    'description': """Milestone Task""",
    'sequence': 1,
    'category': 'Milestone Task',
    'installable': True,
    'depends': ['project','sale'],
    'data': [
        "views/sale_order_views.xml",
        "views/sale_order_line_views.xml"
    ]
}