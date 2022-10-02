
# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    price_unit_readonly = fields.Boolean(string="Unit Price Readonly", compute="_compute_readonly_priceunit")

    @api.depends('partner_id', 'product_id')
    def _compute_readonly_priceunit(self):
        # if seller.name.id == line.order_id.partner_id.id and seller.product_tmpl_id.id == product.product_tmpl_id.id:
        for line in self:
            line.price_unit_readonly = any(line.product_id.seller_ids.filtered(lambda x: x.name == line.partner_id).mapped('price_unit_readonly'))

