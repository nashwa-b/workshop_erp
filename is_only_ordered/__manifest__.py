# -*- coding: utf-8 -*-

{
    'name': 'Is only ordered',
    'version': '19.0.1.0.0',
    'licence': 'LGPL-3',
    'summary': """Is only ordered""",
    'description': """Is only ordered""",
    'sequence': -10,
    'category': 'Is only ordered',
    'application': True,
    'installable': True,
    'depends': ['base','sale','product'],
    'data': [
        "views/res_partner_views.xml",
        "views/sale_order_line_views.xml"
    ]
}