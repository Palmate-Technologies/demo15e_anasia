from odoo import api, fields, models, _

class ResUsers(models.Model):
    _inherit = 'res.users'

    allowed_warehouse_ids = fields.Many2many('stock.warehouse', 'stock_warehouse_users_rel', 'user_id', 'warehouse_id', string='Allowed Warehouse')
    allowed_location_ids = fields.Many2many('stock.location', 'location_security_stock_location_users', 'user_id', 'location_id', string='Allowed Location', domain=[('usage', '=', 'internal')])
    allowed_picking_type_ids = fields.Many2many('stock.picking.type', 'stock_picking_type_users_rel', 'user_id', 'picking_type_id', string='Allowed Operation Types')

    def _process_warehouse_change(self, values):
        ### ids = [1,2,3] ; locations = [stock.location(1,2,3,)]
        if 'allowed_location_ids' in values.keys():
            location_ids = values.get('allowed_location_ids', False)[0][2]
            picking_types = self.env['stock.picking.type'].search(['|',
                                        ('default_location_src_id','in',tuple(location_ids)),
                                        ('default_location_dest_id','in',tuple(location_ids))])
            values['allowed_picking_type_ids'] = picking_types.ids
            if not location_ids:
                values['allowed_picking_type_ids'] = [(6, 0, [])]

        if 'allowed_warehouse_ids' in values.keys():
            warehouse_ids = values.get('allowed_warehouse_ids', False)[0][2]
            allowed_location_ids, allowed_picking_type_ids = [], []
            for warehouse in self.env['stock.warehouse'].browse(warehouse_ids):
                locations = self.env['stock.location'].search([('id','child_of',warehouse.mapped('view_location_id').ids),('usage','=','internal')])
                allowed_location_ids += locations.ids

                picking_types = self.env['stock.picking.type'].search([('warehouse_id','=',warehouse.id)])
                allowed_picking_type_ids += picking_types.ids
                
            if not warehouse_ids:
                allowed_location_ids = allowed_picking_type_ids = [(6, 0, [])]

            values['allowed_location_ids'] = allowed_location_ids
            values['allowed_picking_type_ids'] = allowed_picking_type_ids

        return values

    def write(self, values):
        for user in self:
            values = user._process_warehouse_change(values)
        return super(ResUsers, self).write(values)