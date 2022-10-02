# -*- coding: utf-8 -*-

from odoo import SUPERUSER_ID, _, api, fields, models
from odoo.exceptions import AccessError, UserError, ValidationError

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    request_order_id = fields.Many2one('request.order', 'Request Order', readonly=True, copy=False)
