# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class account_reconciliation_model_fix(models.Model):
#     _name = 'account_reconciliation_model_fix.account_reconciliation_model_fix'
#     _description = 'account_reconciliation_model_fix.account_reconciliation_model_fix'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
