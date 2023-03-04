from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
from datetime import datetime, timedelta
from odoo.exceptions import UserError

ZAOKRUZENJE = 2

class DateUtil:

    @staticmethod
    def previous_month(date):
        month = date.month
        year = date.year
        if month == 1:
            date = date.replace(month=12, year=year-1)
        else:
            date = date.replace(month=month-1)
        return date

    @staticmethod
    def default_date_from():

        #today = 10.03.2023 => 10.01.2023
        start_date = DateUtil.previous_month(datetime.today().date())
        start_date = DateUtil.previous_month(start_date)
        # 01.01.2023
        return start_date.replace(day=1)

    @staticmethod
    def default_date_to():

        # today = 10.03.2023 => 01.02.2023
        to_date = DateUtil.previous_month(datetime.today().date().replace(day=1))

        # 31.01.2023
        return to_date + timedelta(days=-1)

class PayrollMip1023Wizard(models.TransientModel):

    _name = 'payroll.mip1023.wizard'

    date_from = fields.Date(string="Obračun od:", required=True, default=DateUtil.default_date_from())
    date_to = fields.Date(string="do:", required=True, default=DateUtil.default_date_to())
    # https://www.odoo.com/forum/help-1/how-to-get-current-company-id-odoo-15-202859
    company_id = fields.Many2one(
        "res.company",
        string="Preduzeće:",
        default=lambda self: self.env.user.company_id,
    )
    date_payment = fields.Date(string="Datum isplate:", required=True, default=(datetime.today().date()))
    date_submit = fields.Date(string="Datum podnošenja:", required=True, default=(datetime.today().date()))
    submit_no = fields.Integer(string="Broj zahtjeva:", required=True, default=1)

    employee_ids = fields.Many2many('hr.employee', string='Zaposleni')

    def action_generate_xml(self):
        data = {'date_from': self.date_from,
                'date_to': self.date_to,
                'date_payment': self.date_payment,
                'date_submit': self.date_submit,
                'submit_no': self.submit_no,
                'company_id': self.company_id.id,
                'employee_ids': self.employee_ids.ids,
                'model': self._name,
                'ids': self.ids,
                'docids': []
               }
  
        return self.env.ref('l10n_bs_hr_payroll_fuelboss.mip1023_xml_report').report_action(self, data=data)

class Mip1023Xml(models.AbstractModel):

    # report.module.report_name
    _name = 'report.l10n_bs_hr_payroll_fuelboss.mip1023_xml_template'
    _inherit = 'report.report_xml.abstract'
    _description = "MIP 1023 XML file"

    @api.model
    def generate_report(self, ir_report, docids, data=None):

        date_format = '%Y-%m-%d'

        company_id = self.env['res.company'].search([('id', '=', int(data['company_id']))])
        date_from = data['date_from']
        date_to = data['date_to']
        date_payment = data['date_payment']
        date_submit = data['date_submit']
        # company_id.vat = PDV broj
        company_registry = company_id.company_registry
        company_name = company_id.name
        period_od = datetime.strptime(date_from, date_format).date()
        period_do = datetime.strptime(date_to, date_format).date()
        sifra_djelatnosti = company_id.work_code

        operacija = "Prijava_od_strane_poreznog_obveznika"
        broj_zahtjeva = data['submit_no']

        datum_isplate = datetime.strptime(date_payment, date_format).date()

        datum_podnosenja = datetime.strptime(date_submit, date_format).date()
        datum_upisa = datum_podnosenja
        datum_unosa = datum_podnosenja

        broj_uposlenih = 0
        pio = 0
        zdr = 0
        zap = 0
        zdr_2 = 0
        prihod = 0
        dopr = 0
        lic_odb = 0
        por = 0

        docs = []
        domain = []
        domain.append(('company_id', '=', company_id.id))
        domain.append(('date_from', '=', datetime.strptime(date_from, DATE_FORMAT).date()))
        domain.append(('date_to', '=', datetime.strptime(date_to, DATE_FORMAT).date()))
        payslips = self.env['hr.payslip'].search(domain, order='name asc')

        for payslip in payslips:
            dopr_iz_svi = round(payslip.dopr_iz_pio + payslip.dopr_iz_zdr + payslip.dopr_iz_zap, ZAOKRUZENJE)
            if type(payslip.employee_id.address_home_id.city_id.code) is not str:
                raise UserError(payslip.employee_id.name + ": city_id.code? " + payslip.employee_id.address_home_id.city_id.name)
            o = {
                'vrsta_isplate': payslip.mip_vrsta_isplate,
                'jmb': payslip.employee_id.identification_id,
                'ime_prezime': payslip.ime_prezime,
                'datum_isplate': datum_isplate,
                'radni_sati': payslip.neto_sati,
                'radni_sati_bolovanje': payslip.bol_preko_sati,
                'bruto_placa': payslip.bruto_osn,
                'koristi_i_drugi_oporezivi_prihodi': 0,
                'ukupan_prihod': payslip.bruto_osn,
                'iznos_pio': payslip.dopr_iz_pio,
                'iznos_zo': payslip.dopr_iz_zdr,
                'iznos_nezaposlenost': payslip.dopr_iz_zap,
                'doprinosi': dopr_iz_svi,
                'prihod_umanjen_za_doprinose': round(payslip.bruto_osn - dopr_iz_svi, ZAOKRUZENJE),
                'koef_lo': payslip.koef_lo,
                'iznos_lo': payslip.iznos_lo,
                'osnovica_poreza': payslip.porez_osn,
                'iznos_porez': payslip.porez,
                'radni_sati_ut': 0,
                'stepen_uvecanja': 0,
                'sifra_radnog_mjesta_ut': '',
                'dopr_pio_mio_ut': 0,
                'beneficirani_rad_staz': False,
                'opcina_prebivalista': payslip.employee_id.address_home_id.city_id.code.strip()
                }
            
            broj_uposlenih += 1
            pio += payslip.dopr_iz_pio
            zdr += payslip.dopr_iz_zdr
            zap += payslip.dopr_iz_zap
            dopr += dopr_iz_svi
            lic_odb += payslip.iznos_lo
            por += payslip.porez
            prihod += payslip.bruto_osn
            docs.append(o)

        data = {
            'company_id': company_registry,
            'company_name': company_name,
            'broj_zahtjeva': broj_zahtjeva, 
            'datum_podnosenja': datum_podnosenja,
            'datum_upisa': datum_upisa,
            'datum_unosa': datum_unosa,
            'datum_isplate': datum_isplate,
            'broj_uposlenih': broj_uposlenih,
            'period_od': period_od,
            'period_do': period_do,
            'sifra_djelatnosti': sifra_djelatnosti,
            'pio': round(pio, ZAOKRUZENJE),
            'zdr': round(zdr, ZAOKRUZENJE),
            'zap': round(zap, ZAOKRUZENJE),
            'zdr_2': round(zdr_2, ZAOKRUZENJE),
            'prihod': round(prihod, ZAOKRUZENJE),
            'dopr': round(dopr, ZAOKRUZENJE),
            'lic_odb': round(lic_odb, ZAOKRUZENJE),
            'por': round(por, ZAOKRUZENJE),
            'operacija': operacija, 
            #'doc_model': data['model'],
            #'doc_ids': data['ids'],
            'docs': docs,
        }

        return super(Mip1023Xml, self).generate_report(ir_report, docids, data)
