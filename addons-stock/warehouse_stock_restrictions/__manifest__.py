# -*- coding: utf-8 -*-
{
    'name': "Warehouse Stock Restrictions.",

    'summary': """Warehouse and Stock Location Restriction on Users.""",

    'description': """
        	Warehouse and Stock Location Restriction on Users.
    """,

    'author': "Palmate",
    'website': "http://www.palmate.in",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Warehouse',
    'version': '0.1',
    'license': 'AGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['stock','sale','base_user_access_limitation','purchase','account'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/users_view.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
