# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.osv import expression
from odoo.exceptions import UserError

class PickingType(models.Model):
    _inherit = "stock.picking.type"

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        if self.env.user.allowed_picking_type_ids:
            args += [('id', 'in', tuple(self.env.user.allowed_picking_type_ids.ids))]
        return super(PickingType, self).search(args=args, offset=offset, limit=limit, order=order, count=count)

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        if self.env.user.allowed_picking_type_ids:
            domain += [('id', 'in', tuple(self.env.user.allowed_picking_type_ids.ids))]
        return super(PickingType, self).read_group(domain, fields, groupby, offset=offset, limit=limit, orderby=orderby,lazy=lazy)

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        if operator not in ('ilike', 'like', '=', '=like', '=ilike'):
            return super(PickingType, self).name_search(name, args, operator, limit)
        new_args = args or []
        if self.env.user.allowed_picking_type_ids:
            new_args.append(('id', 'in', tuple(self.env.user.allowed_picking_type_ids.ids)))
        return super(PickingType, self).name_search(name=name, args=new_args, operator=operator, limit=limit)
