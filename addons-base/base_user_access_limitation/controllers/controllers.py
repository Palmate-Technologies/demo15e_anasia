# -*- coding: utf-8 -*-
from odoo import http

# class BaseUserAccessLimitation(http.Controller):
#     @http.route('/base_user_access_limitation/base_user_access_limitation/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/base_user_access_limitation/base_user_access_limitation/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('base_user_access_limitation.listing', {
#             'root': '/base_user_access_limitation/base_user_access_limitation',
#             'objects': http.request.env['base_user_access_limitation.base_user_access_limitation'].search([]),
#         })

#     @http.route('/base_user_access_limitation/base_user_access_limitation/objects/<model("base_user_access_limitation.base_user_access_limitation"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('base_user_access_limitation.object', {
#             'object': obj
#         })