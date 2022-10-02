from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_uom_category_id = fields.Many2one(related='uom_id.category_id')
    allowed_uom_ids = fields.Many2many('uom.uom', string='Allowed UoM',
                                       domain="[('category_id', '=', product_uom_category_id)]",
                                       help='These Uoms will only be available to select in Sales/Purchase orders.')
