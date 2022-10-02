# -*- coding: utf-8 -*-
###################################################################################
#
#    This program is free software: you can modify
#    it under the terms of the GNU Affero General Public License (AGPL) as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
###################################################################################
from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    def _filter_access_rules_python(self, operation):
        res = super(ProductTemplate, self)._filter_access_rules_python(operation)

        if operation in ("create", "write") and not self.env.user.has_group("product_edit_restrict.data_group_product_manager"):
            return self.env[self._name]

        return res

