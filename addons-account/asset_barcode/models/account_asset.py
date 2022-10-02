# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo import models, fields

class AccountAsset(models.Model):
    _inherit = 'account.asset'
    
    serial_number = fields.Char(string='Serial number')
    barcode = fields.Char(string='Barcode')

