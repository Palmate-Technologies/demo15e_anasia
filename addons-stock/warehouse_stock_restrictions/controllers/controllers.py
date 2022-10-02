# -*- coding: utf-8 -*-
# from odoo import http


# class WarehouseStockRestrictions(http.Controller):
#     @http.route('/warehouse_stock_restrictions/warehouse_stock_restrictions/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/warehouse_stock_restrictions/warehouse_stock_restrictions/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('warehouse_stock_restrictions.listing', {
#             'root': '/warehouse_stock_restrictions/warehouse_stock_restrictions',
#             'objects': http.request.env['warehouse_stock_restrictions.warehouse_stock_restrictions'].search([]),
#         })

#     @http.route('/warehouse_stock_restrictions/warehouse_stock_restrictions/objects/<model("warehouse_stock_restrictions.warehouse_stock_restrictions"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('warehouse_stock_restrictions.object', {
#             'object': obj
#         })
