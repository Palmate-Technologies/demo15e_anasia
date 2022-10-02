# -*- coding: utf-8 -*-
{
    'name': "Cost Price Fluctuation Restriction",

    'summary': "Allows to set Cost price fluctuation in percent, warns if price goes beyond limit.",

    'author': "Palmate",

    'description': """
Allows to set Cost price fluctuation in percent, warns if price goes beyond limit.
Ignores the check if either cost price is 0 or the available stock is 0.
""",
    'category': 'Purchase',
    'version': '15.0.0.1',
    'website': "https://www.palmate.in",
    'license': 'AGPL-3',

    'depends': ['sale', 'purchase', 'stock_base'],

    'data': [
        # 'views/res_config_settings.xml',
        'views/product_views.xml',
    ],

    'demo': [
        'demo/demo.xml',
    ],
}
