from odoo import fields, models, api

class HrPayslipFB(models.Model):

    _inherit = "hr.payslip"
    
    mip_vrsta_isplate = fields.Selection([
        ('1', '1 - Isplata samo plate'),
        ('2', '2 - Plate, koristi i ostale isplate'),
        ('3', '3 - nakn roditeljsko/porodiljsko poslodavac'),
        ('4', '4 - nakn roditelj/porodilj Centri za soc rad'),
        ('5', '5 - nakn bolovanje preko 42d poslodavac'),
        ('6', '6 - nakn bolovanje preko 42d Zavod zdr osig direktno'),
        ('7', '7 - isplata plate invalidne osobe'),
        ('8', '8 - isplata doprinosa detaširani zaposlenici'),
        ('9', '9 - kombinacija 1 i 3 ili 2 i 3 - roditelj'),
        ('10', '10 - kombinacija 1 i 5 ili 2 i 5 - bolov preko 42d'),
        ('11', '11 - doprinosi PIO za zaposlene Brčko Distrikt'),
        ('12', '12 - doprinosi zdr,zap rezidenti FBiH obavljaju u PC'),
        ('13', '13 - doprinosi PIO,zdr,zap rezidenti FBiH obavljaju u BrčD'),
        ('14', '14 - kombinacija 1 i 8 ili 2 i 8 - detaširani'),
        ('15', '15 - isplata po čl 27. stav 5 Zakona'),
      ], 'MIP vrsta isplate', compute='_compute_mip_vrsta_isplate',
         search='_search_mip_vrsta_isplate',
         groups="hr.group_hr_user", store=False)

    email = fields.Char('Email', compute='_compute_email',
                        search='_search_email', 
                        store=False)

    @api.depends('state')
    def _compute_mip_vrsta_isplate(self):

        for payslip in self:
            detasirani = False
            redovni = False
            bol_preko = False
            rod_ods = False
            vrsta = 1
            for line in payslip.line_ids:
                if line.total > 0:
                    if line.code == 'REDRAD':
                        redovni = True
                    elif line.code == 'BOL_PREKO':
                        bol_preko = True 
                    elif line.code == 'ROD_ODS':
                        rod_ods = True      
                # detasirani
                if 'INO' in line.contract_id.struct_id.code:
                   detasirani = True
            if redovni:
                if detasirani:
                    vrsta = 14
                else:
                    vrsta = 1

            if bol_preko:
                if redovni:
                    vrsta = 10 # kombinacija
                else:
                    vrsta = 5

            if rod_ods:
                if redovni:
                    vrsta = 9
                else:
                    vrsta = 3

            if detasirani and not redovni:
                vrsta = 8
          
            payslip.mip_vrsta_isplate = str(vrsta)

    @api.depends('employee_id')
    def _compute_email(self):

        for payslip in self:
            payslip.email = payslip.employee_id.work_email or payslip.employee_id.private_email


    def _search_mip_vrsta_isplate(self, operator, value):

        #recs = self.env['hr.payslip'].search([], limit=None)
        if operator == '!=':
           recs = self.search([]).filtered(lambda x: x.mip_vrsta_isplate != value)
        else:
           recs = self.search([]).filtered(lambda x : x.mip_vrsta_isplate == value)

        return [('id', 'in', [x.id for x in recs])]


    def _search_email(self, operator, value):

        if operator == '!=':
           recs = self.search([]).filtered(lambda x: x.email != value)
        else:
           # npr '@' - sadrzi
           recs = self.search([]).filtered(lambda x: x.email and value in x.email)
        return [('id', 'in', [x.id for x in recs])]
