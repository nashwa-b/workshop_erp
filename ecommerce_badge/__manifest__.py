# -*- coding: utf-8 -*-

{
    'name': 'eCommerce Badge',
    'version': '19.0.1.0.0',
    'licence': 'LGPL-3',
    'summary': """Ecommerce Badge""",
    'description': """Ecommerce Badge""",
    'sequence': -10,
    'category': 'ecommerce badge',
    'installable': True,
    'depends': ['base','product','website_sale'],
    'data': [
        'security/ir.model.access.csv',
        "views/product_template_views.xml",
        "views/badge_template_views.xml"
    ]
}


