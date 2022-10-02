from odoo import api, fields, models

class Users(models.Model):
    _inherit = "res.users"
    
    def assign_to_group(self, group):
        group.write({'users': [(4, self.id)]})
        
    def remove_from_group(self, group):
        group.write({'users': [(3, self.id)]})