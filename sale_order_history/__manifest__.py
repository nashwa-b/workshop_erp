# -*- coding: utf-8 -*-

{
    'name': 'Sale Order History',
    'version': '19.0.1.0.0',
    'licence': 'LGPL-3',
    'summary': """Sale Order History""",
    'description': """Sale Order Historys""",
    'sequence': -10,
    'category': 'sale order history',
    'applictaion': True,
    'installable': True,
    'depends': ['base','sale','product','purchase'],
    'data': ['security/ir.model.access.csv',
                'data/ir_cron_data.xml',
             'views/sale_purchase_history_views.xml'
    ]
}