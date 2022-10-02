from odoo import api, fields, models

class ShowStockWizard(models.TransientModel):
    _name = "show.stock.wizard"
    _description = "Show Stock Wizard"

    wizard_lines = fields.One2many("show.stock.wizard.lines", "wizard_id", readonly=True)
    out_of_stock = fields.Boolean(string="Out of Stock")
    
    @api.model
    def default_get(self, fields_list):
        purchase_line = self.env['purchase.order.line'].browse(self._context.get('active_id'))
        res = super(ShowStockWizard, self).default_get(fields_list)
        wizard_lines, out_of_stock = [], True
        for location in self.env['stock.location'].search([('usage', '=', 'internal')]):
            qty_available = purchase_line.product_id.with_context(location=location.id).qty_available or 0
            unit_of_measure = purchase_line.product_id.with_context(location=location.id).uom_id or False
            if not qty_available:
                continue
            line = (0, 0, {
                'location_id': location.id,
                'quantity': qty_available,
                'uom_id': unit_of_measure,
            })
            wizard_lines.append(line)
            out_of_stock = False

        res.update({'wizard_lines': wizard_lines, 'out_of_stock':out_of_stock})
        return res


class ShowStockWizardLines(models.TransientModel):
    _name = "show.stock.wizard.lines"
    _description = "Show Stock Wizard Lines"

    location_id = fields.Many2one("stock.location", string="Location", readonly=True)
    quantity = fields.Float(string="Quantity", readonly=True)
    uom_id = fields.Many2one("uom.uom", string="UoM", readonly=True)

    wizard_id = fields.Many2one("show.stock.wizard", string="Wizard", readonly=True)

