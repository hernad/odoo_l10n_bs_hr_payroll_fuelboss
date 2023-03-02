from odoo import fields, models

class EmployeeFB(models.Model):
    #_inherit = ['hr.employee.base', 'mail.thread', 'mail.activity.mixin', 'resource.mixin', 'avatar.mixin']
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
    ], 'Stručna sprema', default='04', groups="hr.group_hr_user", tracking=True)

    private_city = fields.Char(related='address_home_id.city', string="Opština stanovanja", readonly=True, related_sudo=False)
    private_state_id = fields.Char(related='address_home_id.state_id.name', string="Kanton stanovanja", readonly=True, related_sudo=False)
    code = fields.Char("Šifra", tracking=True)

 