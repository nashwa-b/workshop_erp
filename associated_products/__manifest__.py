# -*- coding: utf-8 -*-

{
    'name': 'Associated Products',
    'version': '19.0.1.0.0',
    'licence': 'LGPL-3',
    'summary': """Associated Products""",
    'description': """Associated products""",
    'sequence': -10,
    'category': 'Products',
    'application': True,
    'installable': True,
    'depends': ['base','product','sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_views.xml',
        'views/res_partner_views.xml',
    ]
}


