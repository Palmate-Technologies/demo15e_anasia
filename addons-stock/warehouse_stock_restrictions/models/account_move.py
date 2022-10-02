# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError

class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.model
    def _default_warehouse_id(self):
        # !!! Any change to the default value may have to be repercuted
        # on _init_column() below.
        return self.env.user._get_default_warehouse_id()

    warehouse_id = fields.Many2one('stock.warehouse', string='Warehouse', readonly=True, check_company=True,
                                   default=_default_warehouse_id)