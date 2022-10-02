{
    'name': 'Account Journal Item Category',
    'summary': """
        Add product category in Journal Items
    """,
    'description': """
        Add product category in Journal Items
    """,
    'category': 'Accounting',
    'version': '15.0.0.1',
    'author': 'Palmate',
    'website': "www.palmate.in",
    'license': 'AGPL-3',

    'depends': ['account', 'product'],

    'data': [
        'views/account_move_views.xml',
    ],



    'installable': True,
    'auto_install': False,
    'application': False,
}
# Video Explanation: https://www.youtube.com/watch?v=BDepk0LhVuI&list=PLqRRLx0cl0hoJhjFWkFYowveq2Zn55dhM&index=1
