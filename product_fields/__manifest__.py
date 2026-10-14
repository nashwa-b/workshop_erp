# -*- coding: utf-8 -*-

{
    'name': 'Product Fields',
    'version': '19.0.1.0.0',
    'licence': 'LGPL-3',
    'summary': """Product Fields""",
    'description': """Product Fields""",
    'sequence': -10,
    'category': 'product fields',
    'applictaion': True,
    'installable': True,
    'depends': ['base','sale','product'],
    'data': [
        "security/ir.model.access.csv",
        "views/res_partner_views.xml",
    "views/sale_order_line_views.xml",
    "views/product_template_views.xml"]
}