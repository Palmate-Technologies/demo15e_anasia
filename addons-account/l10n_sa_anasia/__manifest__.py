# -*- coding: utf-8 -*-
{
    'name': "Saudi Arabia Anasia - Accounting",
    'author': "Palmate",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting/Localizations/Account Charts',
    'version': '15.0',

    # any module necessary for this one to work correctly
    'depends': ['account','l10n_multilang'],

    # always loaded
    'data': [
        'data/account_data.xml',
        'data/account_chart_template_data.xml',
        'data/account.account.template.csv',
        'data/account_tax_group.xml',
        'data/l10n_sa_chart_data.xml',
        'data/account_tax_report_data.xml',
        'data/account_tax_template_data.xml',
        'data/account_fiscal_position_template_data.xml',
        'data/account_chart_template_configure_data.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
