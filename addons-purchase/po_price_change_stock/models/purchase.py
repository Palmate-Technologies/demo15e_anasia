# -*- coding: utf-8 -*-
###################################################################################
#
#    This program is free software: you can modify
#    it under the terms of the GNU Affero General Public License (AGPL) as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
###################################################################################
from odoo import api, fields, models


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    def write(self, values):
        res = super(PurchaseOrderLine, self).write(values)

        if "price_unit" in values:
            for line in self:

                for move in line.move_ids.filtered(lambda m: m.picking_id and m.picking_id.state not in ('done', 'cancel')):
                    price_unit = line._get_stock_move_price_unit()
                    move.write({'price_unit': price_unit})

        return res
