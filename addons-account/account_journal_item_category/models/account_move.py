# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    
    product_category_id = fields.Many2one(string='Product Category', related='product_id.categ_id', store=True)


