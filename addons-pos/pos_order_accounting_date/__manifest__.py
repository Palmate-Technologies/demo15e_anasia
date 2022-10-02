# -*- coding: utf-8 -*-
{
    'name': "Pos Order Accounting Date",
    'summary': " ",
    'author': "Palmate",

    # for the full list
    'category': 'Sales/Point of Sale',
    'version': '15.0.0.1',
    'license': 'AGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'point_of_sale'],

    # always loaded
    'data': [
        'views/pos_order.xml',
        'report/report_pos_order.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
