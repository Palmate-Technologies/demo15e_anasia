{
    'name': 'Asset Location Transfer',
    'summary': """
        -Transfer asset from one location to other.
    """,
    'description': """
        -Transfer asset from one location to other.
    """,
    'category': 'Account',
    'version': '15.0.0.1',
    'author': 'Palmate',
    'website': "www.palmate.in",
    'license': 'AGPL-3',

    'depends': ['account', 'account_asset', 'stock'],

    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/account_asset_views.xml',
        'views/asset_transfer_view.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
