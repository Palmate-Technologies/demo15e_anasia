# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError

class ApprovalApproverBase(models.Model):
    _name = 'approval.approver.base'
    _description = 'Approver Base'

    _check_company_auto = True

    user_id = fields.Many2one('res.users', string="User", required=True, check_company=True, domain="[('id', 'not in', existing_request_user_ids)]")
    existing_request_user_ids = fields.Many2many('res.users', compute='_compute_existing_request_user_ids')
    status = fields.Selection([
        ('new', 'New'),
        ('pending', 'To Approve'),
        ('approved', 'Approved'),
        ('refused', 'Refused'),
        ('cancel', 'Cancel')], string="Status", default="new", readonly=True)
    request_id = fields.Many2one('request.order', string="Request",
        ondelete='cascade', check_company=True)
    company_id = fields.Many2one(
        string='Company', related='request_id.company_id',
        store=True, readonly=True, index=True)
    is_user_turn = fields.Boolean("User Turn")
    sequence = fields.Integer('Sequence')

    def send_email(self):
        if self.user_id.email and self.request_id.approval_type_id and self.request_id.approval_type_id.mail_template_id:
            mail_template = self.request_id.approval_type_id.mail_template_id
            request = self.request_id
            to_emails = [self.user_id.email]
            # if self.user_id.is_vp:
            #     to_emails.append('accounting2@wjeen.com')
            for to_email in to_emails:
                mail_template.write({'email_to': to_email})
                mail_template.send_mail(request.id, force_send=True, raise_exception=False, email_values=None)
                mail_template.write({'email_to': False})


        return True

    @api.model
    def create(self, vals):
        rec = super(ApprovalApproverBase, self).create(vals)
        if rec.is_user_turn:
            rec.send_email()
        return rec

    def write(self, values):
        rec = super(ApprovalApproverBase, self).write(values)
        if 'is_user_turn' in values and values.get('is_user_turn',False) == True:
            self.send_email()
        return rec

    def action_approve(self):
        self.request_id.action_approve(self)

    def action_refuse(self):
        self.request_id.action_refuse(self)

    def _create_activity(self):
        return True
        # for approver in self:
        #     approver.request_id.activity_schedule(
        #         'approvals.mail_activity_data_approval',
        #         user_id=approver.user_id.id)

    @api.depends('request_id.requester_user_id', 'request_id.approver_ids.user_id')
    def _compute_existing_request_user_ids(self):
        for approver in self:
            approver.existing_request_user_ids = \
                self.mapped('request_id.approver_ids.user_id')._origin \
              | self.request_id.requester_user_id._origin
