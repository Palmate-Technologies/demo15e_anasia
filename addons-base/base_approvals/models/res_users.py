# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, models

class Users(models.Model):
    _inherit = "res.users"

    is_vp = fields.Boolean(string="Is Vice President", help="Used in Request order approval process, \n if this user approves request, Requester will be notified")
    is_ceo = fields.Boolean(string="Is CEO", help="Used in Request order approval process, \n if this user approves request, Requester will be notified")
