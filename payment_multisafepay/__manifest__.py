# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Payment Provider: MultiSafepay',
    'version': '1.0',
    'category': 'Accounting/Payment Providers',
    'sequence': 1,
    'summary': "MultiSafepay",
    'description': " ",  # Non-empty string to avoid loading the README file.
    'application':True,
    # 'installable': True,
    # 'author': 'Odoo S.A., Applix BV, Droggol Infotech Pvt. Ltd.',
    # 'website': 'https://www.mollie.com',
    'depends': ['payment'],
    'data': [
        "data/payment_provider_data.xml",
        "views/payment_multisafepay_templates.xml",

        "views/payment_provider_views.xml",
    ],
    'post_init_hook': 'post_init_hook',
    'uninstall_hook': 'uninstall_hook',
    'license': 'LGPL-3'
}