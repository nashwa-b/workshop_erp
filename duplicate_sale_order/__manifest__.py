# -*- coding: utf-8 -*-

{
    'name': 'Duplicate Sale Order',
    'version': '19.0.1.0.0',
    'licence': 'LGPL-3',
    'summary': """Duplicate Sale Order""",
    'description': """Duplicate Sale Order""",
    'sequence': -10,
    'category': 'Duplicate Sale Order',
    'application': True,
    'installable': True,
    'depends': ['base','sale'],
    'data': [
        "data/ir_actions_data.xml"
    ]
}