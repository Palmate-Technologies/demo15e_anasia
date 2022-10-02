
# -*- coding: utf-8 -*-
from odoo import models, fields, api, _


class ProductSupplierinfo(models.Model):
    _inherit = "product.supplierinfo"

    price_unit_readonly = fields.Boolean(string="Unit Price Readonly")


















