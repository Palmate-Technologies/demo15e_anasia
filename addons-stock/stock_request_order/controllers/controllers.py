# -*- coding: utf-8 -*-
# from odoo import http


# class StockRequestOrder(http.Controller):
#     @http.route('/stock_request_order/stock_request_order/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/stock_request_order/stock_request_order/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('stock_request_order.listing', {
#             'root': '/stock_request_order/stock_request_order',
#             'objects': http.request.env['stock_request_order.stock_request_order'].search([]),
#         })

#     @http.route('/stock_request_order/stock_request_order/objects/<model("stock_request_order.stock_request_order"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('stock_request_order.object', {
#             'object': obj
#         })
