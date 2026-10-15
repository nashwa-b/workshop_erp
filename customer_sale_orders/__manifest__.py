# -*- coding: utf-8 -*-

{
    'name': 'Customer Sale Orders',
    'version': '19.0.1.0.0',
    'licence': 'LGPL-3',
    'summary': """Customer Sale Orders""",
    'description': """Sale Orders""",
    'sequence': -10,
    'category': 'customer sale orders',
    'applictaion': True,
    'installable': True,
    'depends': ['base','sale','product'],
    'data': [
        "views/res_partner_views.xml",]
}