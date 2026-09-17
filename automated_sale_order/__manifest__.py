# -*- coding: utf-8 -*-

{
    'name': 'Automated Sale Order',
    'version': '19.0.1.0.0',
    'licence': 'LGPL-3',
    'summary': """Automated sale order in product view""",
    'description': """Automated sale order in product view""",
    'sequence': 1,
    'category': 'Approval blocks',
    # 'application': True,
    'installable': True,
    'depends': ['base','product','sale'],
    'data': [
        'security/ir.model.access.csv',
        'wizard/sale_order_wizard_views.xml',
        'views/product_template_views.xml',
    ]
}
