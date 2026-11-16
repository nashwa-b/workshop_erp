# -*- coding: utf-8 -*-

{
    'name': 'Product Return',
    'version': '19.0.1.0.0',
    'licence': 'LGPL-3',
    'summary': """Product Return""",
    'description': """Product Return""",
    'sequence': -10,
    'category': 'product return',
    'installable': True,
    'application': True,
    'depends': ['base','product','website_sale'],
    'data': [
        'views/product_return_template.xml',
        'views/return_view_template.xml'
        # 'security/ir.model.access.csv',
        # "views/product_template_views.xml",
        # "views/badge_template_views.xml"
    ]
}
