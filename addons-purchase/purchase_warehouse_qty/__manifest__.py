{
    "name": "Purchase Warehouse Qty",
    "summary": "Show Available Qty in purchase order line.",
    "version": "15.0.0.1",
    "author": "Palmate",
    "website": "http://www.palmate.in",
    "category": "Purchase",
    "depends": ["purchase_stock"],
    "data": [
        'security/ir.model.access.csv',
        "views/purchase_views.xml",
        "wizards/show_stock_wizard_views.xml",
    ],
    'demo': [],
    "license": "AGPL-3",
    "installable": True,
    # "application": False,
}
