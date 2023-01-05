from odoo import fields, models

class EmployeeFB(models.Model):
    _inherit = 'hr.employee'
    _description = "Employee fuelboss"

    _sql_constraints = [
        ('code_uniq', 'unique (code, company_id)', "Šifra zaposlenog u preduzeću mora biti jedinstvena.")
    ]

    certificate = fields.Selection([
        ('01', 'NK'),
        ('02', 'PK'),
        ('03', 'KV'),
        ('04', 'SSS'),
        ('05', 'VKV'),
        ('06', 'VŠ'),
        ('07', 'VSS'),
    ], 'Stručna sprema', default='other', groups="hr.group_hr_user", tracking=True)

    code = fields.Char("Šifra", tracking=True)
