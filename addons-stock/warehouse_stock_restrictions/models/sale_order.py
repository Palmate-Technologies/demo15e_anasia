from odoo import api, fields, models, _

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        if self.env.user.allowed_warehouse_ids:
            args.append(('warehouse_id', 'in', tuple(self.env.user.allowed_warehouse_ids.ids)))
        return super(SaleOrder, self).search(args=args, offset=offset, limit=limit, order=order, count=count)

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        if self.env.user.allowed_warehouse_ids:
            domain += [('warehouse_id', 'in', tuple(self.env.user.allowed_warehouse_ids.ids))]
        return super(SaleOrder, self).read_group(domain, fields, groupby, offset=offset, limit=limit, orderby=orderby,lazy=lazy)

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        if operator not in ('ilike', 'like', '=', '=like', '=ilike'):
            return super(SaleOrder, self).name_search(name, args, operator, limit)
        new_args = args or []
        if self.env.user.allowed_warehouse_ids:
            new_args.append(('warehouse_id', 'in', tuple(self.env.user.allowed_warehouse_ids.ids)))
        return super(SaleOrder, self).name_search(name=name, args=new_args, operator=operator, limit=limit)

    # def _prepare_invoice(self):
    #     invoice_vals = super(SaleOrder, self)._prepare_invoice()
    #     invoice_vals['warehouse_id'] = self.warehouse_id and self.warehouse_id.id or False
    #     return invoice_vals
