# -*- coding: utf-8 -*-
{
    'name': "Base Approvals",

    'summary': """
        This is base module for managing approval requests.
""",

    'description': """
        This is base module for managing approval requests.
    """,

    'author': "Palmate",
    'website': "http://www.palmate.in",

    # for the full list
    'category': 'Base',
    'version': '15.0.0.1',
    'license': 'AGPL-3',

    # any module necessary for this one to work correctly
    'depends': ['stock','mail', 'account', 'approvals'],

    # always loaded
    'data': [
        'security/security_view.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'data/mail_data.xml',

        'views/approval_types_view.xml',
        'views/request_order_view.xml',
        'views/user_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
