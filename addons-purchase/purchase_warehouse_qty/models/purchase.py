from odoo import _, api, fields, models

class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    def show_warehouse_stock(self):
        return {
            'name': 'Warehouse Stock',
            'domain': [],
            'res_model': 'show.stock.wizard',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'context': {},
            'target': 'new',
        }


