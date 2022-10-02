# -*- coding: utf-8 -*-

from odoo import SUPERUSER_ID, _, api, fields, models
from odoo.exceptions import AccessError, UserError, ValidationError

class ApprovalUsers(models.Model):
    _name = 'approval.users'
    _description = 'Approval users'
    _order = 'id'

    name = fields.Integer('Sequence')
    user_id = fields.Many2one('res.users', 'User', copy=False)
    approval_type_id = fields.Many2one('approval.types', 'Approval Type', copy=False)


class ApprovalType(models.Model):
    _name = 'approval.types'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Approval Type'
    _order = 'id'

    name = fields.Char('Name')
    description = fields.Char('Description')
    acquire_method = fields.Selection(string='Acquire Method', selection=[])
    company_id = fields.Many2one('res.company', 'Company', copy=False)
    picking_type_id = fields.Many2one('stock.picking.type', 'Operation Type', copy=False, required=True)

    is_manager_approver = fields.Boolean(
        string="Employee's Manager",
        help="Automatically add the manager as approver on the request.")
    # user_ids = fields.Many2many('res.users', string="Approvers",
    #     check_company=True, domain="[('company_ids', 'in', company_id)]")
    approval_users = fields.One2many('approval.users', 'approval_type_id', string="Approvers")
    approval_minimum = fields.Integer(string="Minimum Approval", default="1", required=True)
    mail_template_id = fields.Many2one('mail.template', 'Mail Template', copy=False, help="if selected, Approver will be notified by email to approve the request.")