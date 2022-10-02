# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PosOrder(models.Model):
    _inherit = 'pos.order'
    _description = 'Point Of Sale Accounting Date'

    accounting_date = fields.Date(string='Accounting Date', readonly=True)

class PosSession(models.Model):
    _inherit = 'pos.session'

    # inherited to add accounting_date field in pos orders
    def close_session_from_ui(self, bank_payment_method_diff_pairs=None):
        res = super(PosSession, self).close_session_from_ui(bank_payment_method_diff_pairs=None)
        accounting_date = self.move_id.date
        self.order_ids.write({'accounting_date': accounting_date})
        return res
