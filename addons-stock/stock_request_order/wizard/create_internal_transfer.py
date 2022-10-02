# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.exceptions import UserError

class CreateInternalTransfer(models.TransientModel):
    _name = 'create.internal.transfer'
    _description = 'Create Internal Transfer'

    name = fields.Char('Name')
    picking_type_id = fields.Many2one('stock.picking.type', 'Deliver To')
    location_id = fields.Many2one('stock.location', 'Source Location', domain=[('usage','=','internal')])
    location_dest_id = fields.Many2one('stock.location', 'Destination Location', domain=[('usage','=','internal')])
    user_id = fields.Many2one('res.users', 'Owner')

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        request_order = self.env[self._context.get('active_model')].browse(self._context.get('active_id'))
        if 'picking_type_id' in fields:
            res['picking_type_id'] = request_order.picking_type_id.id
        if 'location_id' in fields:
            res['location_id'] = request_order.picking_type_id.default_location_src_id.id
        if 'location_dest_id' in fields:
            res['location_dest_id'] = request_order.picking_type_id.default_location_dest_id.id
            
        return res

    @api.onchange('picking_type_id')
    def onchange_picking_type(self):
        if self.picking_type_id:
            location_id, location_dest_id = False, False
            if self.picking_type_id.default_location_src_id:
                location_id = self.picking_type_id.default_location_src_id.id
            if self.picking_type_id.default_location_dest_id:
                location_dest_id = self.picking_type_id.default_location_dest_id.id
            self.location_id = location_id
            self.location_dest_id = location_dest_id


    def process(self):
        # create transfer here
        Picking = self.env['stock.picking']
        request_order = self.env['request.order'].browse(self._context.get('active_id'))
        
        moves = []
        for line in request_order.request_lines:
            if not (line.product_id or line.approved_qty):
                continue
            uom_id = line.uom_id and line.uom_id.id or False
            if not uom_id:
                uom_id = line.product_id.uom_id.id

            vals = {
                'product_id':line.product_id.id,
                'name': line.name or line.product_id.name,
                'product_uom': uom_id,
                'date': request_order.request_date,
                'product_uom_qty':line.approved_qty,
                'price_unit':line.product_id.standard_price,
                'origin':request_order.name,
                'location_id': self.location_id.id,
                'location_dest_id': self.location_dest_id.id,
            }
            moves.append((0,0, vals))

        picking_type_id = self.picking_type_id and self.picking_type_id.id or False
        if not picking_type_id:
            picking_type_id = request_order.picking_type_id and request_order.picking_type_id.id or False
        if not picking_type_id:
            raise UserError(_("Please select Delivery To."))
        picking_vals = {
            'picking_type_id': request_order.picking_type_id.id,
            'location_id': self.location_id.id,
            'location_dest_id': self.location_dest_id.id,
            'move_ids_without_package': moves,
            'origin':request_order.name,
            'request_order_id': request_order.id,
        }
        Picking.create(picking_vals)

        # request_order.write({'approver_user_id':self.env.user, 'transfer_count':1})
        request_order.write({'transfer_count':1})
        return True

