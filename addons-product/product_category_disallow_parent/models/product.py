from odoo import models, fields, api
from odoo.exceptions import UserError

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def _check_product_linking(self,vals):
        if vals.get('categ_id', False) and self.env['product.category'].browse(vals.get('categ_id')).disallow_product_linking:
            raise UserError(('Products can not be added to selected category.'))
        return True

    @api.model
    def create(self, vals):
        self._check_product_linking(vals)
        return super(ProductTemplate, self).create(vals)

    def write(self, vals):
        self._check_product_linking(vals)
        return super(ProductTemplate, self).write(vals)