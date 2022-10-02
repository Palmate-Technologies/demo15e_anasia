# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class CreatePurchaseOrder(models.TransientModel):
    _name = 'create.purchase.order.line'
    _description = 'Create Purchase Order Line'
    _rec_name = 'product_id'


    purchase_id = fields.Many2one('create.purchase.order', 'Line')
    product_id = fields.Many2one('product.product', 'Product')
    partner_id = fields.Many2one('res.partner', 'Vendor')
    uom_id = fields.Many2one('uom.uom', string='Unit of Measure')
    qty = fields.Float('Quantity', digits=0, help='Approved Qty')
    request_line_id = fields.Many2one('request.order.line', 'Req Line')


class CreatePurchaseOrder(models.TransientModel):
    _name = 'create.purchase.order'
    _description = 'Create Purchase Order'

    name = fields.Char('Name')
    line_ids = fields.One2many(
        'create.purchase.order.line',
        'purchase_id',
        string="Lines")

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        if 'line_ids' in fields:
            request_order = self.env[self._context.get('active_model')].browse(self._context.get('active_id'))
            line_ids = []
            for line in request_order.request_lines:
                partner_id = False
                if line.product_id.seller_ids:
                    partner = line.product_id.seller_ids[0].name or False
                    if partner: partner_id = partner.id
                d={
                    'product_id': line.product_id.id,
                    'partner_id': partner_id,
                    'qty': line.approved_qty,
                    'uom_id': line.uom_id and line.uom_id.id or False,
                    'request_line_id': line.id,
                }
                line_ids.append((0, 0, d))
            res['line_ids'] = line_ids
            
        return res

    def _prepare_purchase_vals(self, request_order, partner):
        purchase_vals = {
            'partner_id': partner.id,
            'picking_type_id': request_order.picking_type_id.id,
            'request_order_id': request_order.id,
            'partner_ref': request_order.name,
        }
        return purchase_vals

    def _prepare_purchase_line_vals(self, request_order, line, purchase_id):
        price_unit = line.product_id.standard_price or 0.0,
        req_lines = request_order.request_lines.filtered(lambda l: l.product_id.id == line.product_id.id)
        if req_lines:
            price_unit = req_lines[0].price_unit

        line_vals = {
            'product_id': line.product_id.id,
            'product_qty': line.qty,
            'product_uom': line.uom_id and line.uom_id.id or False,
            'price_unit': price_unit,
            'order_id': purchase_id,
        }
        return line_vals


    def process(self):
        # create PO here
        partners = self.line_ids.mapped('partner_id')
        if not partners:
            raise UserError(_('Please select Vendor to create Purchase.'))

        Purchase = self.env['purchase.order']
        Purchaseline = self.env['purchase.order.line']
        request_order = self.env['request.order'].browse(self._context.get('active_id'))
        purchase_count = 0
        for partner in partners:

            purchase_vals = self._prepare_purchase_vals(request_order, partner)
            new_purchase = Purchase.create(purchase_vals)

            for line in self.line_ids.filtered(lambda l: l.partner_id.id == partner.id):
                if not (line.product_id or line.qty):
                    continue
                line_vals = self._prepare_purchase_line_vals(request_order, line, new_purchase.id)
                purchase_line = Purchaseline.create(line_vals)

                req_lines = line.request_line_id
                # req_lines = request_order.request_lines.filtered(lambda l: l.product_id.id == line.product_id.id)
                if req_lines:
                    write_vals = {
                        'approved_qty':line.qty,
                        'requested_qty':line.qty,
                        'purchase_line_id':purchase_line.id
                    }
                    req_lines.write(write_vals)

            purchase_count += 1
        request_order.write({'purchase_count': purchase_count})
        return True

    # def process(self):
    #     # create PO here
    #     partners = self.line_ids.mapped('partner_id')
    #     Purchase = self.env['purchase.order']
    #     request_order = self.env['request.order'].browse(self._context.get('active_id'))
    #     purchase_count = 0
    #     for partner in partners:
    #         order_lines = []
    #         for line in self.line_ids.filtered(lambda l: l.partner_id.id==partner.id):
    #             if not (line.product_id or line.qty):
    #                 continue
    #             price_unit = line.product_id.standard_price or 0.0,
    #             req_lines = request_order.request_lines.filtered(lambda l: l.product_id.id==line.product_id.id)
    #             if req_lines:
    #                 req_lines.write({'approved_qty':line.qty})
    #                 price_unit = req_lines[0].price_unit
    #             line_vals = {
    #                 'product_id':line.product_id.id,
    #                 'product_qty':line.qty,
    #                 'product_uom':line.uom_id and line.uom_id.id or False,
    #                 'price_unit': price_unit,
    #             }
    #
    #             order_lines.append((0,0,line_vals))
    #
    #         purchase_vals = {
    #             'partner_id': partner.id,
    #             'picking_type_id': request_order.picking_type_id.id,
    #             'order_line': order_lines,
    #             'request_order_id': request_order.id,
    #             'partner_ref': request_order.name,
    #         }
    #         Purchase.create(purchase_vals)
    #         purchase_count += 1
    #     request_order.write({'purchase_count': purchase_count})
    #     return True

