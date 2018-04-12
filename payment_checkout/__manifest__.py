# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Checkout.com Payment Acquirer',
    'category': 'Payment Acquirer',
    "author" : "Parikshit Vaghasiya",
    'summary': 'Payment Acquirer: Checkout.com Implementation',
    'description': """
    Checkout.com Payment Acquirer.

    """,
    'depends': ['payment'],
    'data': [
        'views/payment_views.xml',
        'views/payment_checkout_templates.xml',
        'data/payment_acquirer_data.xml',
    ],
}
