from odoo import fields, models

class PartnerFB(models.Model):
    _inherit = 'res.partner'
    _description = "Partner fuelboss"

    _sql_constraints = [
        ('name_unique', 'unique(type,name)', 'Ime u adresaru mora biti jedinstveno.')
    ]
