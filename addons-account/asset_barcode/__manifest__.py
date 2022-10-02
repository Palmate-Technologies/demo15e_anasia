{
    'name': 'Asset Barcode',
    'summary': """
    -Adds Barcode and  Serial number fields in assets.
    """,
    'description': """
        -Adds Barcode and  Serial number fields in assets.
    """,
    'category': 'Account',
    'version': '15.0.0.1',
    'author': 'Palmate',
    'website': "www.palmate.in",
    'license': 'AGPL-3',

    'depends': ['account', 'account_asset'],

    'data': [
        'views/account_asset_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
