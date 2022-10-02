# -*- coding: utf-8 -*-

from odoo import SUPERUSER_ID, _, api, fields, models
from odoo.exceptions import AccessError, UserError, ValidationError

class RequestOrderLine(models.Model):
    _inherit = 'request.order.line'

    purchase_line_id = fields.Many2one('purchase.order.line', 'Purchase Order Line')

class RequestOrder(models.Model):
    _inherit = 'request.order'

    purchase_orders = fields.One2many('purchase.order', 'request_order_id', 'Purchase Orders')
    stock_pickings = fields.One2many('stock.picking', 'request_order_id', 'Transfers')

    purchase_count = fields.Integer(string='Purchase Count', copy=False, default=0)
    transfer_count = fields.Integer(string='Transfer Count', copy=False, default=0)


    @api.onchange('acquire_method')
    def onchange_acquire_method(self):
        res = {}
        if self.acquire_method == 'purchase_order':
            res = {'domain': {'picking_type_id': [('code', '=', 'incoming')]}}
        if self.acquire_method == 'internal_transfer':
            res = {'domain': {'picking_type_id': [('code', '=', 'internal')]}}
        return res

    def _cancel_related_document(self):
        for rec in self:
            if rec.request_status=='approved':
                if rec.acquire_method == 'purchase_order':
                    purchases = rec.purchase_orders
                    if purchases:
                        if purchases.filtered(lambda p: p.state not in ('draft','cancel')):
                            raise ValidationError(
                                _("Can not cancel now, as Purchase Order is already confirmed."))
                        purchases.button_cancel()
                    # rec.write({'purchase_orders': [(6, 0, [])], 'purchase_count':0})
                    rec.write({'purchase_count':0}) # TODO confirm this
                if rec.acquire_method == 'internal_transfer':
                    pickings = rec.stock_pickings
                    if pickings:
                        if pickings[0].state not in ('draft','cancel'):
                            raise ValidationError(
                                _("Can not cancel now, as Transfer picking is already confirmed."))
                        pickings.action_cancel()
                    rec.write({'stock_pickings': [(6, 0, [])], 'transfer_count':0})
        return True

    def action_cancel(self):
        self._cancel_related_document()
        return super(RequestOrder, self).action_cancel()

    def action_withdraw(self, approver=None):
        self._cancel_related_document()
        return super(RequestOrder, self).action_withdraw()

    def action_create_purchase_order(self):
        view = self.env.ref('stock_request_order.view_create_purchase_order_form')
        return {
            'name': _('Purchases'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'create.purchase.order',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'context': {},
        }
        return True
    
    def action_create_internal_transfer(self):
        view = self.env.ref('stock_request_order.view_create_internal_transfer_form')
        return {
            'name': _('Internal Transfer'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'create.internal.transfer',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'context': {},
        }
        return True

    def action_view_purchases(self):
        purchase_order_ids = self.purchase_orders and self.purchase_orders.ids or []
        if purchase_order_ids:
            result = self.env['ir.actions.act_window']._for_xml_id('purchase.purchase_form_action')
            # choose the view_mode accordingly
            if len(purchase_order_ids) > 1:
                result['domain'] = [('id', 'in', purchase_order_ids)]
            elif len(purchase_order_ids) == 1:
                res = self.env.ref('purchase.purchase_order_form', False)
                form_view = [(res and res.id or False, 'form')]
                if 'views' in result:
                    result['views'] = form_view + [(state, view) for state, view in result['views'] if view != 'form']
                else:
                    result['views'] = form_view
                result['res_id'] = purchase_order_ids[0]
            else:
                result = {'type': 'ir.actions.act_window_close'}

            return result

    def action_view_transfers(self):
        picking_ids = self.stock_pickings and self.stock_pickings.ids or []
        if picking_ids:
            result = self.env['ir.actions.act_window']._for_xml_id('stock.action_picking_tree_all')
            # choose the view_mode accordingly
            if len(picking_ids) > 1:
                result['domain'] = [('id', 'in', picking_ids)]
            elif len(picking_ids) == 1:
                res = self.env.ref('stock.view_picking_form', False)
                form_view = [(res and res.id or False, 'form')]
                if 'views' in result:
                    result['views'] = form_view + [(state, view) for state, view in result['views'] if view != 'form']
                else:
                    result['views'] = form_view
                result['res_id'] = picking_ids[0]
            else:
                result = {'type': 'ir.actions.act_window_close'}

            return result

    ## Report functions
    def action_print_request_order(self):
        return self.env.ref('stock_request_order.action_report_request_order').report_action(self)

    def _get_line_details(self, line):
        po_line = line.purchase_line_id or False
        bill_no = ''
        qty_received, qty_invoiced = 0, 0
        if po_line:
            qty_received = po_line.qty_received or 0.0
            qty_invoiced = po_line.qty_invoiced or 0.0
            moves = po_line.invoice_lines.mapped('move_id')
            if moves:
                bill_no = moves[0].name

        res = {
            'po_no':line.purchase_line_id and line.purchase_line_id.order_id.name or '',
            'bill_no':bill_no,
            'qty_received': qty_received,
            'qty_invoiced':qty_invoiced,
        }
        # self.purchase_orders
        return res

    def _get_amount_paid(self):
        total = due = 0
        move_ids = []
        for line in self.request_lines:
            po_line = line.purchase_line_id or False
            if po_line:
                moves = po_line.invoice_lines.mapped('move_id')
                move_ids +=  moves.ids
        if move_ids:
            moves = self.env['account.move'].browse(list(set(move_ids)))
            total = sum(moves.mapped('amount_total'))
            due = sum(moves.mapped('amount_residual'))

        return total - due

    ## Report functions