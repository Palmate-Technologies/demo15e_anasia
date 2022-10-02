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
from itertools import groupby


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    # splitted = fields.Boolean(default=False)

    def split_picking_on_availability(self):
        unavailable_dict = {}
        for picking in self:
            if picking.picking_type_id.split_on_availability:# and not picking.splitted:
                # picking.splitted = True

                # Remove Unavailable
                for line in picking.move_ids_without_package:
                    unavailable = line.product_uom_qty - line.product_id.qty_available
                    if unavailable > 0:
                        unavailable_dict[line.product_id.id] = unavailable
                        line.product_uom_qty = line.product_id.qty_available

        # Create Unavailable
        if unavailable_dict:
            self.create_unavailable_picking(unavailable_dict)

    def create_unavailable_picking(self, unavailable_dict):
        picking = self.copy()

        picking.backorder_id = self.id

        # print(hasattr(self, 'pos_session_id'))

        # if hasattr(self, 'pos_session_id'):
        #     picking.pos_session_id = self.pos_session_id.id
            # print('1', self.pos_session_id)

        for line in picking.move_ids_without_package:
            if line.product_id.id in unavailable_dict:
                for p in unavailable_dict:
                    if line.product_id.id == p:
                        line.product_uom_qty = unavailable_dict[p]
            else:
                if line.state != "draft":
                    line._action_cancel()
                line.unlink()

    # def action_confirm(self):
    def _action_done(self):

        for picking in self:
            if picking.picking_type_id.split_on_availability:
                for move in picking.move_ids_without_package:
                    if move.product_uom_qty == 0:
                        move._action_cancel()
                        move.unlink()
        #
    #     block
        res = super(StockPicking, self)._action_done()
        return res

    def write(self, vals):
        if "pos_session_id" in vals:
            backorder = self.env['stock.picking'].search([('backorder_id', '=', self.id)])
            if backorder and not backorder.pos_session_id:
                backorder.pos_session_id = vals['pos_session_id']

        return super(StockPicking, self).write(vals)


class StockMove(models.Model):
    _inherit = 'stock.move'

    def _action_confirm(self, merge=True, merge_into=False):

        # print('2', self.picking_id.pos_session_id)
        for move in self:
            move.picking_id.split_picking_on_availability()

        res = super(StockMove, self)._action_confirm(merge=merge, merge_into=merge_into)

        # print('3', self.picking_id.pos_session_id)
        return res

