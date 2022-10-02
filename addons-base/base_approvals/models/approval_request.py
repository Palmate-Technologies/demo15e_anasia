# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models

class ApprovalRequest(models.Model):
    _inherit = 'approval.request'

    approver_ids = fields.One2many('approval.approver', 'request_id', string="Approvers", check_company=True, readonly=True)
