# -*- coding: utf-8 -*-
{
    'name': "Stock Request Order",

    'summary': """
        Stock Request order.
""",

    'description': """
        Stock Request order.
    """,

    'author': "Palmate",
    'website': "http://www.palmate.in",

    # for the full list
    'category': 'Stock',
    'version': '15.0.0.1',
    'license': 'AGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base','stock','purchase','base_approvals'],

    # always loaded
    'data': [
        # 'security/security_view.xml',
        'security/ir.model.access.csv',

        # 'data/ir_sequence_data.xml',
        'views/request_order_view.xml',
        'wizard/create_purchase_order_view.xml',
        'wizard/create_internal_transfer_view.xml',
        'report/report_request_order.xml',
        'report/report_request_order_amounts.xml',
        'report/report.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
