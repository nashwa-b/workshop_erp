# -*- coding: utf-8 -*-

{
    'name': 'Material Request',
    'version': '19.0.1.0.0',
    'licence': 'LGPL-3',
    'summary': """Material Request""",
    'description': """Material Request""",
    'sequence': 1,
    'category': 'Material Request',
    'application': True,
    'installable': True,
    'depends': ['base','purchase'],
    'data': [
        "security/ir.model.access.csv",
        "views/material_request_views.xml",
        "views/purchase_order_views.xml"
    ]
}
