from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
from datetime import datetime, timedelta

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

    date_from = fields.Date(string="Od", required=True, default=DateUtil.default_date_from())
    date_to = fields.Date(string="Do", required=True, default=DateUtil.default_date_to())
    
    employee_ids = fields.Many2many('hr.employee', string='Zaposleni')

    def action_generate_xml(self):
        data = {'date_from': self.date_from, 
                'date_to': self.date_to, 
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

        docs = []
        employees = self.env['hr.employee'].search([], order='name asc')
        for employee in employees:
            if data['employee_ids']:
                # samo oni koji su u formi odabrani
                if employee.id in data['employee_ids']:
                    docs.append({
                        'name': employee.name,
                        'code': employee.code
                    })
            else:
                # svi zaposleni
                docs.append({
                    'name': employee.name,
                    'code': employee.code
                })

        date_from = datetime.strptime(data['date_from'], DATE_FORMAT).date()
        date_to = datetime.strptime(data['date_to'], DATE_FORMAT).date()

        company_id="4218139660005"
        company_name="Fuelboss doo Zenica"
        broj_zahtjeva="1"
        broj_uposlenih=299
        operacija = "Prijava_od_strane_poreznog_obveznika"
        broj_zahtjeva = 1
        datum_podnosenja = '2023-01-01'
        datum_upisa = '2023-01-02'
        datum_unosa = '2023-01-04'
        datum_isplate='2023-01-03'
        broj_uposlenih=2
        period_od='2023-01-01'
        period_do='2023-01-31'
        sifra_djelatnosti='25.511'
        pio = 10000
        zdr = 80000
        zap = 20000
        zdr_2 = 0
        prihod = 50000
        dopr = 300009
        lic_odb = 3800
        por = 19000

        docs = []
        o = {
            'vrsta_isplate': 1,
            'jmb': '010101',
            'ime_prezime': 'ernad husremovic',
            'datum_isplate': datum_isplate,
            'radni_sati': 176,
            'radni_sati_bolovanje': 0,
            'bruto_placa': round(1526,2),
            'koristi_i_drugi_oporezivi_prihodi': 0,
            'ukupan_prihod': round(1526,2),
            'iznos_pio': 100,
            'iznos_zo': 80,
            'iznos_nezaposlenost': 10,
            'doprinosi': 190,
            'prihod_umanjen_za_doprinose': 1300,
            'koef_lo': 1,
            'iznos_lo': 300,
            'osnovica_poreza': 200,
            'iznos_porez': 20,
            'radni_sati_ut': 0,
            'stepen_uvecanja': 0,
            'sifra_radnog_mjesta_ut': '',
            'dopr_pio_mio_ut': 0,
            'beneficirani_rad_staz': False, 
            'opcina_prebivalista': '103'
        }
        docs.append(o) 
       
        o = {
            'vrsta_isplate': 8,
            'jmb': '010101',
            'ime_prezime': 'meho mehic',
            'datum_isplate': datum_isplate,
            'radni_sati': 168,
            'radni_sati_bolovanje': 8,
            'bruto_placa': round(1526,2),
            'koristi_i_drugi_oporezivi_prihodi': 0,
            'ukupan_prihod': round(1526,2),
            'iznos_pio': 100,
            'iznos_zo': 80,
            'iznos_nezaposlenost': 10,
            'doprinosi': 190,
            'prihod_umanjen_za_doprinose': 1300,
            'koef_lo': 1,
            'iznos_lo': 300,
            'osnovica_poreza': 200,
            'iznos_porez': 20,
            'radni_sati_ut': 0,
            'stepen_uvecanja': 0,
            'sifra_radnog_mjesta_ut': '',
            'dopr_pio_mio_ut': 0,
            'beneficirani_rad_staz': False, 
            'opcina_prebivalista': '103'
        }
        docs.append(o)

        data = {
            'company_id': company_id,
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
            'pio': pio,
            'zdr': zdr,
            'zap': zap,
            'zdr_2': zdr_2,
            'prihod': prihod,
            'dopr': dopr,
            'lic_odb': lic_odb,
            'por': por,
            'operacija': operacija, 
            #'doc_model': data['model'],
            #'doc_ids': data['ids'],
            'docs': docs,
        }

        return super(Mip1023Xml, self).generate_report(ir_report, docids, data)
