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


class StockImmediateTransfer(models.TransientModel):
    _inherit = 'stock.immediate.transfer'

    def process(self):

        # Find Picking
        pickings = self.env['stock.picking']
        for line in self.immediate_transfer_line_ids:
            pickings |= line.picking_id

        for picking in pickings:

            if picking.picking_type_id.code != 'outgoing':
                continue

            # Distinguish Moves
            available_move_ids = self.env['stock.move']
            unavailable_move_ids = self.env['stock.move']

            for line in picking.move_lines:
                if line.product_id.qty_available >= line.product_uom_qty:
                    available_move_ids |= line
                else:
                    unavailable_move_ids |= line

            # Split Picking
            if available_move_ids and unavailable_move_ids:

                new_picking = picking.copy({
                    'name': '/',
                    'move_lines': [],
                    'move_line_ids': [],
                    'backorder_id': picking.id,
                })

                unavailable_move_ids.package_level_id.write({'picking_id': new_picking.id})
                unavailable_move_ids.write({'picking_id': new_picking.id})

        res = super(StockImmediateTransfer, self).process()
        return res


class StockBackorderConfirmation(models.TransientModel):
    _inherit = 'stock.backorder.confirmation'

    def process(self):

        # # Find Picking
        for picking in self.pick_ids:

            if picking.picking_type_id.code != 'outgoing':
                continue

            # Distinguish Moves
            available_move_ids = self.env['stock.move']
            unavailable_move_ids = self.env['stock.move']

            for line in picking.move_lines:

                qty_to_move = line.product_uom_qty

                if line.quantity_done:
                    qty_to_move = line.quantity_done

                if line.product_id.qty_available >= qty_to_move:
                    available_move_ids |= line
                else:
                    unavailable_move_ids |= line

            # Split Picking
            if available_move_ids and unavailable_move_ids:

                new_picking = picking.copy({
                    'name': '/',
                    'move_lines': [],
                    'move_line_ids': [],
                    'backorder_id': picking.id,
                })

                unavailable_move_ids.package_level_id.write({'picking_id': new_picking.id})
                unavailable_move_ids.write({'picking_id': new_picking.id})

        res = super(StockBackorderConfirmation, self).process()
        return res

