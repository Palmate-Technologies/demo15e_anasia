from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class AssetTransfer(models.Model):
    _name = 'asset.transfer'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(string="Name", readonly=True, index=True, required=True, copy=False,
                       default=lambda self: _('New'))
    asset_id = fields.Many2one('account.asset', string='Asset', required=True)
    create_date = fields.Date('Creation Date', default=fields.Datetime.now)
    location_id = fields.Many2one('stock.location', string='Source Location', readonly=True)
    location_dest_id = fields.Many2one('stock.location', string='Destination Location', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Status', default="draft")
    reason = fields.Text(string="Reason")


    @api.constrains('location_id', 'location_dest_id')
    def src_dest_location_diff(self):
        for rec in self:
            if rec.location_id and rec.location_dest_id:
                if rec.location_id.id == rec.location_dest_id.id:
                    raise ValidationError(_("Please select different source and destination location !"))

    def action_done(self):
        self.state = 'done'
        if self.asset_id:
            self.asset_id.location_id = self.location_dest_id or False

    def action_cancel(self):
        for asset in self:
            asset.state = 'cancel'

    def set_to_draft(self):
        """
            sent the status of Asset Transfer request in Set to Draft state
        """
        self.write({
            'state': 'draft',
            })

    @api.onchange('asset_id')
    def _onchange_asset_id(self):
        if self.asset_id:
            self.location_id = self.asset_id.location_id or False

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('asset.transfer') or 'New'
        return super(AssetTransfer, self).create(vals)


