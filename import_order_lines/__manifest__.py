# -*- coding: utf-8 -*-

{
    'name': 'Import Order Lines',
    'version': '19.0.1.0.0',
    'licence': 'LGPL-3',
    'summary': """Import order lines into sale""",
    'description': """Import order lines into sale""",
    'sequence': 1,
    'category': 'Import Lines',
    'application': True,
    'installable': True,
    'depends': ['base','sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_views.xml',
        'wizard/import_lines_wizard_views.xml'

    ]
}
