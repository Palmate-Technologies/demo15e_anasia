from odoo import models, fields

class ProductCategory(models.Model):
    _inherit = 'product.category'

    disallow_product_linking = fields.Boolean('Disallow Product Linking')