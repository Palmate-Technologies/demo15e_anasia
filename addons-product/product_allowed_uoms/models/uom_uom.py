# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import api, fields, tools, models, _

class UoM(models.Model):
    _inherit = 'uom.uom'

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        if operator not in ('ilike', 'like', '=', '=like', '=ilike'):
            return super(UoM, self).name_search(name, args, operator, limit)
        new_args = args or []
        if self._context.get('product_id', False):
            product = self.env['product.product'].browse(self._context['product_id'])
            allowed_uoms = self.env['uom.uom']
            allowed_uoms |= product.uom_id
            allowed_uoms |= product.uom_po_id
            if product.allowed_uom_ids:
                allowed_uoms |= product.allowed_uom_ids
            new_args.append(('id', 'in', allowed_uoms.ids))
        return super(UoM, self).name_search(name=name, args=new_args, operator=operator, limit=limit)