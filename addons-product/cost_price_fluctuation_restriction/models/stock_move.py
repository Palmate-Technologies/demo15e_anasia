# -*- coding: utf-8 -*-
from odoo import models, _
from odoo.exceptions import UserError

class StockMove(models.Model):
    _inherit = 'stock.move'

    def _finalize_product_price_update_before_done(self, new_std_price, product_tot_qty_available):
        product = self.product_id
        allowed_cp_variation = product.allowed_cp_variation_perc
        old_price = product.standard_price or 0
        if not allowed_cp_variation or not old_price or not product_tot_qty_available:
            return True
        cp_variation = (abs(new_std_price - old_price)) / old_price * 100
        if cp_variation > allowed_cp_variation:
            raise UserError(_("New cost price exceeded the allowed variation range! Please check UoM or price unit for: %s", product.name + " (" + product.default_code + ")"))

        return super()._finalize_product_price_update_before_done(new_std_price, product_tot_qty_available)


