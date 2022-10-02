# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
class AccountAsset(models.Model):
    _inherit = 'account.asset'
    
    location_id = fields.Many2one('stock.location', string='Location', readonly=True)
    transfer_count = fields.Integer(string='Transfer Count', compute='_get_transfer')
    asset_transfers = fields.One2many('asset.transfer', 'asset_id', 'Transfers')

    @api.depends('asset_transfers.asset_id')
    def _get_transfer(self):
        transfer_count = 0
        if self.asset_transfers:
            transfer_count = len(self.asset_transfers.ids)
        self.transfer_count = transfer_count


    def action_view_transfer(self):
        self.ensure_one()
        asset_transfers = self.asset_transfers
        return {
            "type": "ir.actions.act_window",
            "res_model": "asset.transfer",
            "views": [[False, "tree"], [False, "form"]],
            "domain": [['id', 'in', asset_transfers.ids]],
            "name": "Asset Transfer",
        }

