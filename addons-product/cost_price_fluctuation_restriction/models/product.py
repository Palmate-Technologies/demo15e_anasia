# -*- coding: utf-8 -*-
from odoo import models, fields, api
from collections import defaultdict
from odoo.tools import float_is_zero, OrderedSet
from odoo.exceptions import UserError
from odoo.tools.translate import _

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    allowed_cp_variation_perc = fields.Float(string="Allowed CP Variation (%)", default=20.0, digits='Product Price')