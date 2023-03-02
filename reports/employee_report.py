from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
from datetime import datetime, timedelta

## transient model for
#class PayrollFbReportWizard(models.TransientModel):
#    _name = 'payroll.fuelboss.report.wizard'
#
#    date_from = fields.Date('Datum od', required=True)
#    date_to = fields.Date('Datum do', required=True)
#    employee_ids = fields.Many2many('hr.employee', string='Zaposleni')
#
#
#    # Generate xlsx report
#    def action_generate_xlsx_report(self):
#        data = {
#            'date_from': self.date_from,
#            'date_to': self.date_to,
#            'employee_ids': self.employee_ids.ids
#        }
#        return self.env.ref('l10n_bs_hr_payroll_fuelboss.action_payroll_fuelboss_xlsx_report').report_action(self, data=data)


class PayrollFbReportPDFWizard(models.TransientModel):

    _name = 'payroll.fuelboss.wizard.pdf'

    date_from = fields.Date(string="Start Date", required=True, default=(datetime.today() + timedelta(days=-7)))
    date_to = fields.Date(string="End Date", required=True, default=fields.Date.today)
    employee_ids = fields.Many2many('hr.employee', string='Zaposleni')

    # generate PDF report
    def action_print_pdf_report(self):
        data = {'date_from': self.date_from, 
                'date_to': self.date_to, 
                'employee_ids': self.employee_ids.ids,
                'model': self._name,
                'ids': self.ids
               }
  
        return self.env.ref('l10n_bs_hr_payroll_fuelboss.report_fuelboss_pdf').report_action(self, data=data)



class EmployeeReportPDF(models.AbstractModel):

    #<report
    #    id="report_fuelboss_pdf"
    #    model="payroll.fuelboss.wizard.pdf"
    #    string="PDF Report"
    #    report_type="qweb-pdf"
    #    name="l10n_bs_hr_payroll_fuelboss.payroll_fuelboss_pdf_report"
    #    file="payroll_fuelboss_pdf"
    #/>
    #
    # report.module.report_name
    _name = 'report.l10n_bs_hr_payroll_fuelboss.payroll_fuelboss_pdf_report'


    @api.model
    def _get_report_values(self, docids, data=None):
        #if not self.env.user.has_group('openacademy.group_manager_openacademy'):
        #    raise UserError('You do not have access to print this report!')

        # sessions = self.env['openacademy.session'].browse(docids)
        # for session in sessions:
        #     if len(session.attendee_ids) == 0:
        #         raise UserError(f"{session.display_name} have no attendees!")
        #return {
        #    'doc_ids': docids,
        #    'doc_model': 'hr.employee',
        #    'docs': self.env['hr.employee'].browse(docids),
        #}

        # get the report action back as we will need its data
        #report = self.env['ir.actions.report']._get_report_from_name('l10n_bs_hr_payroll_fuelboss.report_fuelboss_pdf')
        # get the records selected for this rendering of the report
        #obj = self.env[report.model].browse(docids)
        # return a custom rendering context

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

        return {
            'date_from': date_from,
            'date_to': date_to,
            'doc_model': data['model'],
            'doc_ids': data['ids'],
            'docs': docs,
        }
    


#class PayrollFbReportXlsx(models.AbstractModel):
#    _name = 'payroll.fuelboss.report.xlsx'
#    _inherit = 'report.report_xlsx.abstract'
#
#    # generate PDF report
#    def action_print_pdf_report(self):
#        data = {'date_from': self.date_from, 
#                'date_to': self.date_to, 
#                'employee_ids': self.employee_ids.ids
#               }
#        return self.env.ref('l10n_bs_hr_payroll_fuelboss.action_payroll_fuelboss_pdf_report').report_action(self, data=data)
#
#    def generate_xlsx_report(self, workbook, data, partners):
#        domain = []
#        #domain = [('state', '!=', 'cancel')]
#        #if data.get('date_from'):
#        #    domain.append(('course_date', '>=', data.get('date_from')))
#        #if data.get('date_to'):
#        #    domain.append(('course_date', '<=', data.get('date_to')))
#        #if data.get('course_ids'):
#        #    domain.append(('id', 'in', data.get('course_ids')))
#        #if data.get('responsible_id'):
#        #    domain.append(('responsible_id', '=', data.get('responsible_id')))
#
#        sheet = workbook.add_worksheet('Plate Fuelboss Report')
#        bold = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': '#fffbed', 'border': True})
#        title = workbook.add_format({'bold': True, 'align': 'center', 'font_size': 20, 'bg_color': '#f2eee4', 'border': True})
#        header_row_style = workbook.add_format({'bold': True, 'align': 'center', 'border': True})
#
#        sheet.merge_range('A1:F1', 'Plate Report', title)
#
#        employees = self.env['hr.employee'].search(domain)
#        row = 3
#        col = 0
#
#        # Header row
#        sheet.set_column(0, 5, 18)
#        sheet.write(row, col, 'kolona 1', header_row_style)
#        sheet.write(row, col+1, 'kolona 2', header_row_style)
#        sheet.write(row, col+2, 'kolona 3', header_row_style)
#        sheet.write(row, col+3, 'kolona 4', header_row_style)
#        sheet.write(row, col+4, 'kolona 5', header_row_style)
#        sheet.write(row, col+5, 'kolona 6', header_row_style)
#        row += 2
#        #for employee in employees:
#        #    if employee.employee_ids:
#        #        sheet.merge_range(f"A{row}:F{row}", employee.name, bold)
#        #    for employee in employee.employee_ids:
#        #        sheet.write(row, col, session.name)
#        #        sheet.write(row, col+1, session.start_date)
#        #        sheet.write(row, col+2, session.duration)
#        #        sheet.write(row, col+3, session.seats)
#        #        sheet.write(row, col+4, session.instructor_id.name)
#        #        sheet.write(row, col+5, session.number_of_attendees())
#        #        row += 1
#        #    if course.session_ids:
#        #        row += 1
#
