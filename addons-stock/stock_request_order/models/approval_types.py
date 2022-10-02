# -*- coding: utf-8 -*-

from odoo import SUPERUSER_ID, _, api, fields, models
from odoo.exceptions import AccessError, UserError, ValidationError

class ApprovalType(models.Model):
    _inherit = 'approval.types'

    acquire_method = fields.Selection(selection_add=[
            ('purchase_order', 'Purchase Order'),
            ('internal_transfer', 'Internal Transfer')])
    # picking_type_id = fields.Many2one('stock.picking.type', 'Operation Type', copy=False)

    @api.onchange('acquire_method')
    def onchange_acquire_method(self):
        res = {}
        if self.acquire_method == 'purchase_order':
            res = {'domain': {'picking_type_id': [('code', '=', 'incoming')]}}
        if self.acquire_method == 'internal_transfer':
            res = {'domain': {'picking_type_id': [('code', '=', 'internal')]}}
        return res