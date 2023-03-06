from odoo import fields, models, api

ZAOKRUZENJE = 2

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

    neto_sati = fields.Float(string="Neto sati", compute="_compute_neto_sati", store=False)
    bol_preko_sati = fields.Float(string="Bolovanje preko 42d sati", compute="_compute_bol_preko_sati", store=False)

    dopr_iz_pio = fields.Float(string="Doprinosi PIO IZ", compute="_compute_dopr_iz_pio", store=False)
    dopr_iz_zdr = fields.Float(string="Doprinosi ZDR IZ", compute="_compute_dopr_iz_zdr", store=False)
    dopr_iz_zap = fields.Float(string="Doprinosi ZAP IZ", compute="_compute_dopr_iz_zap", store=False)

    porez_osn = fields.Float(string="Porezna osnovica", compute="_compute_porez_osn", store=False)
    koef_lo = fields.Float(string="Koef LO", compute="_compute_koef_lo", store=False)
    iznos_lo = fields.Float(string="Iznos LO", compute="_compute_iznos_lo", store=False)
    porez = fields.Float(string="Porez", compute="_compute_porez", store=False)

    dopr_pio = fields.Float(string="Doprinos PIO", compute="_compute_dopr_pio", store=False)
    dopr_zdr = fields.Float(string="Doprinos ZDR", compute="_compute_dopr_zdr", store=False)
    dopr_zap = fields.Float(string="Doprinos ZAP", compute="_compute_dopr_zap", store=False)
    bruto_osn = fields.Float(string="Bruto", compute="_compute_bruto_osn", store=False)
    neto_prije = fields.Float(string="Neto prije", compute="_compute_neto_prije", store=False)
    neto_poslije = fields.Float(string="Neto poslije", compute="_compute_neto_poslije", store=False)
    to_naknada = fields.Float(string="TO naknada", compute="_compute_to_naknada", store=False)
    ukupno = fields.Float(string="Ukupno", compute="_compute_ukupno", store=False)

    ime_prezime = fields.Char(string="Ime i Prezime", compute="_compute_ime_prezime", store=False)


    @api.depends('state')
    def _compute_mip_vrsta_isplate(self):

        for payslip in self:
            bol_preko_sati = False
            rod_ods_sati = False
            vrsta = 1
            # neto sati po detasiranom ugovoru
            detasirani_neto_s = False
            # neto sati u BiH (nisu ukljuceni sati BOL_PREKO)
            bih_neto_s = False
            for line in payslip.line_ids:
                if line.total != 0 or line.quantity != 0:
                    if line.code == 'BOL_PREKO':
                        bol_preko_sati = True
                    elif line.code == 'ROD_ODS':
                        rod_ods_sati = True
                    # detasirani
                    if 'INO' in line.contract_id.struct_id.code:
                        if line.code == 'NETO_S':
                            detasirani_neto_s = True
                    else:
                        if line.code == 'NETO_S':
                            bih_neto_s = True

            if bih_neto_s:
                if detasirani_neto_s:
                    vrsta = 14
                else:
                    vrsta = 1

            if bol_preko_sati:
                if bih_neto_s:
                    # kombinacija bol_preko + redovni
                    vrsta = 10
                else:
                    vrsta = 5

            if rod_ods_sati:
                if bih_neto_s:
                    vrsta = 9
                else:
                    vrsta = 3

            if detasirani_neto_s and not bih_neto_s:
                vrsta = 8
          
            payslip.mip_vrsta_isplate = str(vrsta)

    def _compute_ime_prezime(self):
        for payslip in self:
            name = payslip.employee_id.name
            payslip.ime_prezime = name[:name.find('(')-1].strip() + ' ' + name[name.find(')')+1:].strip()

    @api.depends('employee_id')
    def _compute_email(self):

        for payslip in self:
            payslip.email = payslip.employee_id.work_email or payslip.employee_id.private_email


    def _search_mip_vrsta_isplate(self, operator, value):

        #recs = self.env['hr.payslip'].search([], limit=None)
        if operator == '!=':
           recs = self.search([]).filtered(lambda x: x.mip_vrsta_isplate != value)
        else:
           recs = self.search([]).filtered(lambda x: x.mip_vrsta_isplate == value)

        return [('id', 'in', [x.id for x in recs])]


    def _search_email(self, operator, value):

        if operator == '!=':
           recs = self.search([]).filtered(lambda x: x.email != value)
        else:
           # npr '@' - sadrzi
           recs = self.search([]).filtered(lambda x: x.email and value in x.email)
        return [('id', 'in', [x.id for x in recs])]


    def rate_d_iz_pio(self, date_from):
        domain = [('date_from', '=', date_from),('code', '=', 'D_IZ_PIO'),('total', '>', 0)]
        lines = self.env["hr.payslip.line"].search(domain, limit=1)
        if len(lines) == 1:
            return lines[0].rate/100
        else:
            return 0

    def rate_d_iz_zdr(self, date_from):
        domain = [('date_from', '=', date_from),('code', '=', 'D_IZ_ZDR'),('total', '>', 0)]
        lines = self.env["hr.payslip.line"].search(domain, limit=1)
        if len(lines) == 1:
            return lines[0].rate/100
        else:
            return 0

    def rate_d_iz_zap(self, date_from):
        domain = [('date_from', '=', date_from),('code', '=', 'D_IZ_ZAP'),('total', '>', 0)]
        lines = self.env["hr.payslip.line"].search(domain, limit=1)
        if len(lines) == 1:
            return lines[0].rate/100
        else:
            return 0
    
    def compute_fields(self):
        
        for payslip in self:
            payslip.neto_sati = 0
            payslip.bol_preko_sati = 0
            payslip.dopr_iz_pio = 0
            payslip.dopr_iz_zdr = 0
            payslip.dopr_iz_zap = 0
            payslip.dopr_pio = 0
            payslip.dopr_zdr = 0
            payslip.dopr_zap = 0
            payslip.bruto_osn = 0
            bruto_osn_det = 0
            payslip.koef_lo = 0
            payslip.iznos_lo = 0
            payslip.to_naknada = 0
            payslip.ukupno = 0
            payslip.neto_prije = 0
            payslip.neto_poslije = 0
            payslip.porez = 0
            payslip.porez_osn = 0
            dopr_iz_bih = 0
            # ako ima vise ugovora, licni_odbitak se moze pojaviti vise puta
            # samo jednom se uracunava u iznos licnog odbitka
            lic_odb_potrosen = False
            for line in payslip.line_ids:
                if line.total != 0 or line.quantity != 0:
                    if line.code == 'BOL_PREKO':
                        payslip.bol_preko_sati += line.quantity
                    elif line.code == 'ROD_ODS':
                        pass
                    elif line.code == 'TO':
                        payslip.to_naknada += line.total
                    elif line.code == 'NETO':
                        payslip.neto_prije += line.total
                    elif line.code == 'NETO_POS':
                        payslip.neto_poslije += line.total
                    elif line.code == 'UKUPNO':
                        payslip.ukupno += line.total
                # detasirani
                if 'INO' in line.contract_id.struct_id.code:
                    if line.code == 'NETO_S':
                        payslip.neto_sati += line.quantity
                    elif line.code == 'BR_OSN_DET':
                        bruto_osn_det += line.total
                        # https://docs.python.org/3/library/functions.html#round
                        # Note The behavior of round() for floats can be surprising: for example, round(2.675, 2) gives 2.67 instead of the expected 2.68
                        # za detasirane nisu obracunati doprinosi IZ
                        # zato se moraju obracunati
                        payslip.dopr_iz_pio += round(line.total * self.rate_d_iz_pio(line.date_from), ZAOKRUZENJE)
                        payslip.dopr_iz_zdr += round(line.total * self.rate_d_iz_zdr(line.date_from), ZAOKRUZENJE)
                        payslip.dopr_iz_zap += round(line.total * self.rate_d_iz_zap(line.date_from), ZAOKRUZENJE)
                        
                    elif line.code == 'D_PIO_DNJ':
                        payslip.dopr_pio += line.total
                    elif line.code == 'D_ZDR_DNJ':
                        payslip.dopr_zdr += line.total
                    elif line.code == 'D_ZAP_DNJ':
                        payslip.dopr_zap += line.total

                else:
                    if line.code == 'NETO_S':
                        payslip.neto_sati += line.quantity
                    elif line.code == 'BR_OSN':
                        payslip.bruto_osn += line.total
                    elif line.code == 'D_IZ':
                        dopr_iz_bih += line.total
                    elif line.code == 'LIC_ODB':
                        if not lic_odb_potrosen:
                            payslip.iznos_lo += line.total
                            payslip.koef_lo = line.rate / 100
                            lic_odb_potrosen = True
                    elif line.code == 'POREZ':
                        payslip.porez += line.total
                    elif line.code == 'D_PIO':
                        payslip.dopr_pio += line.total
                    elif line.code == 'D_ZDR':
                        payslip.dopr_zdr += line.total
                    elif line.code == 'D_ZAP':
                        payslip.dopr_zap += line.total
                    elif line.code == 'D_IZ_PIO':
                        payslip.dopr_iz_pio += line.total
                    elif line.code == 'D_IZ_ZDR':
                        payslip.dopr_iz_zdr += line.total
                    elif line.code == 'D_IZ_ZAP':
                        payslip.dopr_iz_zap += line.total

            # detasirani ne ulaze u poreznu osnovicu
            payslip.porez_osn = payslip.bruto_osn - dopr_iz_bih - payslip.iznos_lo
            if payslip.porez_osn < 0:
                payslip.porez_osn = 0
                # gleda se samo dio iznosa LO koji je 'potrosen'
                # payslip.iznos_lo = payslip.bruto_osn - dopr_iz_bih
            # ali na kraju ulaze u ukupno bruto osnovicu
            payslip.bruto_osn += bruto_osn_det

            payslip.neto_sati = round(payslip.neto_sati, ZAOKRUZENJE)
            payslip.bol_preko_sati = round(payslip.bol_preko_sati, ZAOKRUZENJE)
            
            payslip.dopr_iz_pio = round(payslip.dopr_iz_pio, ZAOKRUZENJE)
            payslip.dopr_iz_zdr = round(payslip.dopr_iz_zdr, ZAOKRUZENJE)
            payslip.dopr_iz_zap = round(payslip.dopr_iz_zap, ZAOKRUZENJE)

            payslip.dopr_pio = round(payslip.dopr_pio, ZAOKRUZENJE)
            payslip.dopr_zdr = round(payslip.dopr_zdr, ZAOKRUZENJE)
            payslip.dopr_zap = round(payslip.dopr_zap, ZAOKRUZENJE)

            payslip.bruto_osn = round(payslip.bruto_osn, ZAOKRUZENJE)
            payslip.koef_lo = round(payslip.koef_lo, ZAOKRUZENJE)
            payslip.iznos_lo = round(payslip.iznos_lo, ZAOKRUZENJE)
            payslip.to_naknada = round(payslip.to_naknada, ZAOKRUZENJE)
            payslip.ukupno = round(payslip.ukupno, ZAOKRUZENJE)
            payslip.neto_prije = round(payslip.neto_prije, ZAOKRUZENJE)
            payslip.neto_poslije = round(payslip.neto_poslije, ZAOKRUZENJE)
            payslip.porez = round(payslip.porez, ZAOKRUZENJE)
            payslip.porez_osn = round(payslip.porez_osn, ZAOKRUZENJE)




    def _compute_neto_sati(self):
        self.compute_fields()

    def _compute_bol_preko_sati(self):
        self.compute_fields()

    def _compute_dopr_iz_pio(self):
        self.compute_fields()

    def _compute_dopr_iz_zdr(self):
        self.compute_fields()
    
    def _compute_dopr_iz_zap(self):
        self.compute_fields()

    def _compute_porez_osn(self):
        self.compute_fields()

    def _compute_koef_lo(self):
        self.compute_fields()

    def _compute_iznos_lo(self):
        self.compute_fields()

    def _compute_porez(self):
        self.compute_fields()

    def _compute_dopr_pio(self):
        self.compute_fields()

    def _compute_dopr_zdr(self):
        self.compute_fields()

    def _compute_dopr_zap(self):
        self.compute_fields()

    def _compute_bruto_osn(self):
        self.compute_fields()

    def _compute_neto_prije(self):
        self.compute_fields()

    def _compute_neto_poslije(self):
        self.compute_fields()

    def _compute_to_naknada(self):
        self.compute_fields()

    def _compute_ukupno(self):
        self.compute_fields()