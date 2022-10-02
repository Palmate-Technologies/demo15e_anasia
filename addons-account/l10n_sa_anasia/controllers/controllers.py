# -*- coding: utf-8 -*-
# from odoo import http


# class IwesabeSecondUom(http.Controller):
#     @http.route('/iwesabe_second_uom/iwesabe_second_uom', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/iwesabe_second_uom/iwesabe_second_uom/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('iwesabe_second_uom.listing', {
#             'root': '/iwesabe_second_uom/iwesabe_second_uom',
#             'objects': http.request.env['iwesabe_second_uom.iwesabe_second_uom'].search([]),
#         })

#     @http.route('/iwesabe_second_uom/iwesabe_second_uom/objects/<model("iwesabe_second_uom.iwesabe_second_uom"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('iwesabe_second_uom.object', {
#             'object': obj
#         })
