# -*- coding: utf-8 -*-

from odoo import SUPERUSER_ID, _, api, fields, models
from odoo.exceptions import AccessError, UserError, ValidationError

class RequestOrderLine(models.Model):
    _name = 'request.order.line'
    _description = "Request Order Line"
    _order = 'id'
    _rec_name='product_id'

    # @api.depends('approved_qty', 'price_unit', 'taxes_id')
    # def _compute_amount(self):
    #     for line in self:
    #         taxes = line.taxes_id.compute_all(
    #             line.price_unit,
    #             line.currency_id,
    #             line.approved_qty,
    #             line.product_id,
    #             False)
    #         line.update({
    #             'price_subtotal': taxes['total_excluded'],
    #             'price_total': taxes['total_included'],
    #             'price_tax': sum(t.get('amount', 0.0) for t in taxes.get('taxes', [])),
    #         })

    name = fields.Char('Description', index=True)
    product_id = fields.Many2one('product.product', 'Product', change_default=True)
    requested_qty = fields.Float('Qty Req', digits='Product Unit of Measure', required=True)
    approved_qty = fields.Float('Qty Approved', digits='Product Unit of Measure', required=True)
    request_id = fields.Many2one('request.order', 'Request Order', index=True, required=True, ondelete='cascade')
    product_uom_category_id = fields.Many2one(related='product_id.uom_id.category_id', readonly=True)
    uom_id = fields.Many2one('uom.uom', string='Unit of Measure', domain="[('category_id', '=', product_uom_category_id)]")

    # price_unit = fields.Float(string='Unit Price', required=True, digits='Product Price', default=0.0)
    # price_subtotal = fields.Monetary(compute='_compute_amount', string='Subtotal', store=True)
    # currency_id = fields.Many2one(related='request_id.currency_id', store=True, string='Currency', readonly=True)
    # taxes_id = fields.Many2many('account.tax', string='Taxes', domain=[('active', '=', True)])
    # price_total = fields.Monetary(compute='_compute_amount', string='Total', store=True)
    # price_tax = fields.Float(compute='_compute_amount', string='Tax', store=True)

    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            product = self.product_id
            self.name = product.name
            self.uom_id = product.uom_id or product.uom_po_id
            self.requested_qty = 1
            self.approved_qty = 1
            # self.price_unit = product.standard_price or 0.0
            # self.taxes_id = product.supplier_taxes_id.filtered(lambda r: r.company_id == self.env.company)

    # @api.onchange('requested_qty')
    # def onchange_qty(self):
    #     self.approved_qty = self.requested_qty

    @api.onchange('approved_qty')
    def onchange_qty(self):
        self.requested_qty = self.approved_qty


class RequestOrder(models.Model):
    _name = 'request.order'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Request Order'
    _order = 'id'

    @api.model
    def _read_group_request_status(self, stages, domain, order):
        request_status_list = dict(self._fields['request_status'].selection).keys()
        return request_status_list

    # @api.depends('request_lines.price_total')
    # def _amount_all(self):
    #     for order in self:
    #         amount_untaxed = amount_tax = 0.0
    #         for line in order.request_lines:
    #             line._compute_amount()
    #             amount_untaxed += line.price_subtotal
    #             amount_tax += line.price_tax
    #         currency = order.currency_id or self.env.company.currency_id
    #         order.update({
    #             'amount_untaxed': currency.round(amount_untaxed),
    #             'amount_tax': currency.round(amount_tax),
    #             'amount_total': amount_untaxed + amount_tax,
    #         })

    name = fields.Char('Name', default=lambda self: _('New'), readonly=True, copy=False, index=True)
    requester_user_id = fields.Many2one('res.users', 'Requester', readonly=True, copy=False, default=lambda self: self.env.user)
    # approver_user_id = fields.Many2one('res.users', 'Approver', readonly=True, copy=False)
    approval_type_id = fields.Many2one('approval.types', 'Approval Type', required=True, tracking=True)
    company_id = fields.Many2one(
        string='Company', related='approval_type_id.company_id',
        store=True, readonly=True, index=True)
    # currency_id = fields.Many2one('res.currency', 'Currency', required=True,
    #     default=lambda self: self.env.company.currency_id.id)
    request_date = fields.Datetime('Request Date', default=fields.Datetime.now, readonly=True)
    approved_date = fields.Datetime('Approved Date', readonly=True)
    acquire_method = fields.Selection(related='approval_type_id.acquire_method')
    # picking_type_id = fields.Many2one('stock.picking.type', related='approval_type_id.picking_type_id')
    picking_type_id = fields.Many2one('stock.picking.type', required=True, tracking=True, domain=[('code','!=','outgoing')])
    approval_minimum = fields.Integer(related="approval_type_id.approval_minimum")
    request_status = fields.Selection([
        ('new', 'To Submit'),
        ('pending', 'Submitted'),
        ('approved', 'Approved'),
        ('refused', 'Rejected'),
        ('cancel', 'Cancel'),
    ], default="new", compute="_compute_request_status",
        store=True, tracking=True,
        group_expand='_read_group_request_status')
    user_status = fields.Selection([
        ('new', 'New'),
        ('pending', 'To Approve'),
        ('approved', 'Approved'),
        ('refused', 'Rejected'),
        ('cancel', 'Cancel')], compute="_compute_user_status")

    request_lines = fields.One2many('request.order.line', 'request_id', string="Request Lines", copy=True)
    approver_ids = fields.One2many('approval.approver.base', 'request_id', string="Approvers", check_company=True)
    has_access_to_request = fields.Boolean(string="Has Access To Request", compute="_compute_has_access_to_request")
    #
    # amount_untaxed = fields.Monetary(string='Untaxed Amount', store=True, readonly=True, compute='_amount_all', tracking=True)
    # amount_tax = fields.Monetary(string='Taxes', store=True, readonly=True, compute='_amount_all')
    # amount_total = fields.Monetary(string='Total', store=True, readonly=True, compute='_amount_all')
    # payment_journal_id = fields.Many2one('account.journal', string='Payment Journal', copy=False, domain=[('type','=','cash')])


    def _compute_has_access_to_request(self):
        is_approval_user = self.env.user.has_group('approvals.group_approval_user')
        for request in self:
            request.has_access_to_request = request.requester_user_id == self.env.user and is_approval_user

    @api.depends('approver_ids.status')
    def _compute_user_status(self):
        for approval in self:
            # approval.user_status = approval.approver_ids.filtered(lambda approver: approver.user_id == self.env.user and approver.is_user_turn).status
            status = (approval.approver_ids.filtered(lambda approver: approver.user_id == self.env.user and approver.is_user_turn)).mapped('status')
            if status:
                approval.user_status = (approval.approver_ids.filtered(lambda approver: approver.user_id == self.env.user and approver.is_user_turn)).mapped('status')[0]
            else:
                approval.user_status = 'new'

    @api.depends('approver_ids.status')
    def _compute_request_status(self):
        for request in self:
            status_lst = request.mapped('approver_ids.status')
            minimal_approver = request.approval_minimum if len(status_lst) >= request.approval_minimum else len(status_lst)
            minimal_approver = max(len(status_lst), request.approval_minimum)
            if status_lst:
                if status_lst.count('cancel'):
                    status = 'cancel'
                elif status_lst.count('refused'):
                    status = 'refused'
                elif status_lst.count('new'):
                    status = 'new'
                elif status_lst.count('approved') >= minimal_approver:
                    status = 'approved'
                else:
                    status = 'pending'
            else:
                status = 'new'
            request.request_status = status

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            seq_date = None
            if 'request_date' in vals:
                seq_date = fields.Datetime.context_timestamp(self, fields.Datetime.to_datetime(vals['request_date']))
            vals['name'] = self.env['ir.sequence'].next_by_code('request.order', sequence_date=seq_date) or _('New')
        return super(RequestOrder, self).create(vals)

    def copy(self, default=None):
        rec = super().copy(default)
        rec._onchange_approval_type_id()
        return rec

    # @api.onchange('approval_type_id', 'requester_user_id')
    # def _onchange_approval_type_id(self):
    #     current_users = self.approver_ids.mapped('user_id')
    #     new_users = self.approval_type_id.user_ids
    #     if self.approval_type_id.is_manager_approver:
    #         employee = self.env['hr.employee'].search([('user_id', '=', self.requester_user_id.id)], limit=1)
    #         if employee.parent_id.user_id:
    #             new_users |= employee.parent_id.user_id
    #     for user in new_users - current_users:
    #         self.approver_ids += self.env['approval.approver.base'].new({
    #             'user_id': user.id,
    #             'request_id': self.id,
    #             'status': 'new'})
    @api.onchange('approval_type_id', 'requester_user_id')
    def _onchange_approval_type_id(self):
        if self.approval_type_id:
            # self.approver_ids = []
            current_users = self.approver_ids.mapped('user_id')
            current_user_ids = []
            if current_users:
                current_user_ids = current_users.ids
            approval_users = self.approval_type_id.approval_users
            print("approval_users: ",approval_users)
            if approval_users:
                min_sequence = min(approval_users.mapped('name'))
                for approval_user in approval_users:
                    if approval_user.user_id and approval_user.user_id.id in current_user_ids:
                        continue
                    is_user_turn = False
                    if min_sequence and approval_user.name == min_sequence:
                        is_user_turn=True
                    self.approver_ids += self.env['approval.approver.base'].new({
                        'user_id': approval_user.user_id.id,
                        'request_id': self.id,
                        'status': 'new',
                        'sequence':approval_user.name,
                        'is_user_turn':is_user_turn
                    })
            self.picking_type_id = self.approval_type_id.picking_type_id and self.approval_type_id.picking_type_id.id or False

    def action_confirm(self):
        if len(self.approver_ids) < self.approval_minimum:
            raise UserError(_("You have to add at least %s approvers to confirm your request.", self.approval_minimum))
        approvers = self.mapped('approver_ids').filtered(lambda approver: approver.status == 'new')
        approvers._create_activity()
        approvers.write({'status': 'pending'})
        # self.write({'date_confirmed': fields.Datetime.now()})

    def next_sequence(self, current_sequence, all_sequences):


        new_sequence = current_sequence
        # loop forever
        counter = 0
        while True:
            new_sequence += 1
            if (new_sequence == max(all_sequences)) or counter>=max(all_sequences) or counter >= 9999:
                return max(all_sequences)
            if new_sequence in all_sequences:
                return new_sequence
            counter += 1

    def _do_send_mail(self, mail_template, to_email):
        mail_template.write({'email_to': to_email})
        mail_template.send_mail(self.id, force_send=True, raise_exception=False, email_values=None)
        mail_template.write({'email_to': False})
        return True

    def notify_approvers_of_vp_ceo_approval(self):
        template_name = False
        if self.env.user.is_vp:
            template_name = 'base_approvals.email_template_vp_approved'
        if self.env.user.is_ceo:
            template_name = 'base_approvals.email_template_ceo_approved'
        if template_name:
            try:
                template_id = self.env.ref(template_name)
            except ValueError:
                template_id = False
            if template_id:
                approver = self.mapped('approver_ids').filtered(
                    lambda approver: not approver.user_id.is_vp and not approver.user_id.is_ceo
                )
                send_to_requester = True
                to_emails = []
                for line in approver:
                    user = line.user_id
                    if user.is_vp or user.is_ceo:
                        continue
                    if user.id == self.requester_user_id.id:
                        send_to_requester = False
                    print("send mail")
                    to_emails.append(user.email)
                if send_to_requester:
                    print("send mail")
                    to_emails.append(self.requester_user_id.email)

                for email in to_emails:
                    self._do_send_mail(template_id, email)

        return True

    def notify_of_all_users_approved(self):
        not_approved =self.mapped('approver_ids').filtered(
            lambda approver: approver.status != 'approved')
        # if not self.request_status != 'approved':
        if not_approved:
            return True
        template_id = False
        try:
            template_id = self.env.ref('base_approvals.email_template_all_users_approved')
        except ValueError:
            template_id = False
        if template_id:
            to_emails = ['accounting2@wjeen.com','vp-admin@wjeen.com']  # for now hardcoded this
            for email in to_emails:
                self._do_send_mail(template_id, email)
        return True

    def action_approve(self, approver=None):
        all_sequences = self.mapped('approver_ids').mapped('sequence') or [1]
        current_sequences = self.mapped('approver_ids').filtered('is_user_turn').mapped('sequence') or [1]
        current_sequence = max(current_sequences)
        new_seq = self.next_sequence(current_sequence, all_sequences)
        if not isinstance(approver, models.BaseModel):
            approver = self.mapped('approver_ids').filtered(
                lambda approver: approver.user_id == self.env.user and approver.is_user_turn
            )
        approver.write({'status': 'approved','is_user_turn':False})
        self.write({'approved_date': fields.Datetime.now()})

        # set new sequence is_user_turn=True
        new_approver = self.mapped('approver_ids').filtered(
            lambda approver: approver.is_user_turn!=True and approver.sequence==new_seq)
        new_approver.write({'is_user_turn': True})

        # if approved by VP/CEO, notify Requester and all other approvers
        self.notify_approvers_of_vp_ceo_approval()
        self.notify_of_all_users_approved()

        # self.sudo()._get_user_approval_activities(user=self.env.user).action_feedback()

    def action_refuse(self, approver=None):
        if not isinstance(approver, models.BaseModel):
            approver = self.mapped('approver_ids').filtered(
                lambda approver: approver.user_id == self.env.user
            )
        approver.write({'status': 'refused'})
        self.write({'approved_date': False})
        # self.sudo()._get_user_approval_activities(user=self.env.user).action_feedback()

    def action_withdraw(self, approver=None):
        if not isinstance(approver, models.BaseModel):
            approver = self.mapped('approver_ids').filtered(
                lambda approver: approver.user_id == self.env.user
            )
            # approver = self.mapped('approver_ids')
        approver.write({'status': 'pending'})
        self.write({'approved_date': False})

    def action_draft(self):
        self.mapped('approver_ids').write({'status': 'new'})

    def action_cancel(self):
        # self.sudo()._get_user_approval_activities(user=self.env.user).unlink()
        self.mapped('approver_ids').write({'status': 'cancel'})
        self.write({'approved_date': False})
