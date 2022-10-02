# -*- coding: utf-8 -*-
{
    'name': "Product Allowed UoMs",

    'summary': """
        -Allows to configure UoMs in Product,\n
        -Allows to select only selected Uoms in Sales, Purchase Orders
        """,

    'description': """
        -Allows to configure UoMs in Product,\n
        -Allows to select only selected Uoms in Sales, Purchase Orders
    """,

    'author': "Palmate",
    'website': "http://www.palmate.in",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Product',
    'version': '15.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['base',
                'web_domain_field',
                'product',
                'sale'
                ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/product_views.xml',
        'views/sale_views.xml',
        'views/purchase_views.xml',
        'views/stock_picking_views.xml',
        'views/account_move_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        # 'demo/demo.xml',
    ],
    'license': 'AGPL-3',
}
