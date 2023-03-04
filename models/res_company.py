from odoo import fields, models, api
class ResCompanyFB(models.Model):

    _inherit = "res.company"

    work_code = fields.Char("Šifra djelatnosti")