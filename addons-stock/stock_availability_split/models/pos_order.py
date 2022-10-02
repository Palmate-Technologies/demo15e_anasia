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


# class PosOrder(models.Model):
#     _inherit = 'pos.order'

    # def _create_order_picking(self):
    #     self.ensure_one()
    #     res = super(PosOrder, self)._create_order_picking()
    #
    #     # print(1111111111111111111)
    #     # print(self.picking_ids)
    #
    #     for picking in self.picking_ids:
    #         print(picking)
    #         print(picking.session_id)
    #         backorder = self.env['stock.picking'].search([('backorder_id', '=', picking.id)])
    #         print(backorder)
    #         print()
    #
    #     return res

