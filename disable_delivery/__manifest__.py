# -*- coding: utf-8 -*-

{
    'name': 'Disable delivery',
    'version': '19.0.1.0.0',
    'licence': 'LGPL-3',
    'summary': """Disable delivery""",
    'description': """Disable delivery""",
    'sequence': -10,
    'category': 'disable delivery',
    'applictaion': True,
    'installable': True,
    'depends': ['base','sale','product'],
    'data': [
        "views/sale_order_views.xml"
    ]
}