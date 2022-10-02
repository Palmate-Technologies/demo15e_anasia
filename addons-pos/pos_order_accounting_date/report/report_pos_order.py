from odoo import api, fields, models, tools


class PosOrderReport(models.Model):
    _inherit = 'report.pos.order'
    _description = 'Pos Order Report Accounting Date'

    accounting_date = fields.Date(string='Accounting Date', readonly=True)

    def _select(self):
        return super(PosOrderReport, self)._select() + ',s.accounting_date AS accounting_date'

    def _group_by(self):
        return super(PosOrderReport, self)._group_by() + ',s.accounting_date'