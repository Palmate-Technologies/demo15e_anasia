# -*- coding: utf-8 -*-
# from odoo import http


# class BaseApprovals(http.Controller):
#     @http.route('/base_approvals/base_approvals/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/base_approvals/base_approvals/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('base_approvals.listing', {
#             'root': '/base_approvals/base_approvals',
#             'objects': http.request.env['base_approvals.base_approvals'].search([]),
#         })

#     @http.route('/base_approvals/base_approvals/objects/<model("base_approvals.base_approvals"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('base_approvals.object', {
#             'object': obj
#         })
