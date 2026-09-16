# -*- coding: utf-8 -*-

{
    'name': 'Approval Blocks',
    'version': '19.0.1.0.0',
    'licence': 'LGPL-3',
    'summary': """Approval Blocks""",
    'description': """Approval Blocks""",
    'sequence': -10,
    'category': 'Approval blocks',
    # 'application': True,
    'installable': True,
    'depends': ['base','purchase'],
    'data': [
        'security/ir.model.access.csv',
        'data/approval_block_data.xml',
        'views/purchase_order_views.xml',
    ]
}


