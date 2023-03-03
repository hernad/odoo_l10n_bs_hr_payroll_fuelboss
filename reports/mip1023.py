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
        print("stop")
        #@api.model
        # def _get_report_values(self, docids, data=None):
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

        data = {
            'date_from': date_from,
            'date_to': date_to,
            'doc_model': data['model'],
            'doc_ids': data['ids'],
            'docs': docs,
        }

        return super(Mip1023Xml, self).generate_report(ir_report, docids, data)
