from odoo import models, fields, api

# transient model for
class PayrollFbReportWizard(models.TransientModel):
    _name = 'payroll.fuelboss.report.wizard'

    date_from = fields.Date('Datum od', required=True)
    date_to = fields.Date('Datum do', required=True)
    employee_ids = fields.Many2many('hr.employee', string='Zaposleni')

    # generate PDF report
    def action_print_pdf_report(self):
        data = {'date_from': self.date_from, 
                'date_to': self.date_to, 
                'employee_ids': self.employee_ids.ids
               }
        return self.env.ref('l10n_bs_hr_payroll_fuelboss.action_payroll_fuelboss_pdf_report').report_action(self, data=data)

    # Generate xlsx report
    def action_generate_xlsx_report(self):
        data = {
            'date_from': self.date_from,
            'date_to': self.date_to,
            'employee_ids': self.employee_ids.ids
        }
        return self.env.ref('l10n_bs_hr_payroll_fuelboss.action_payroll_fuelboss_xlsx_report').report_action(self, data=data)


class PayrollFbReportPDF(models.AbstractModel):
    _name = 'report.payroll.fuelboss.pdf'
    def _get_report_values(self, docids, data=None):
        #domain = [('state', '!=', 'cancel')]
        domain = []
        if data.get('date_from'):
            domain.append(('course_date', '>=', data.get('date_from')))
        if data.get('date_to'):
            domain.append(('course_date', '<=', data.get('date_to')))
        if data.get('employee_ids'):
            domain.append(('id', 'in', data.get('employee_ids')))
        docs = self.env['hr.employee'].search(domain)
        employee_ids = self.env['hr.employee'].browse(data.get('employee_ids'))
        data.update({'employees': ",".join([employee.name for employee in employee_ids])})
        return {
            'doc_ids': docs.ids,
            'doc_model': 'hr.employee',
            'docs': docs,
            'datas': data
        }


class PayrollFbReportXlsx(models.AbstractModel):
    _name = 'report.payroll.fuelboss.xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, partners):
        domain = []
        #domain = [('state', '!=', 'cancel')]
        #if data.get('date_from'):
        #    domain.append(('course_date', '>=', data.get('date_from')))
        #if data.get('date_to'):
        #    domain.append(('course_date', '<=', data.get('date_to')))
        #if data.get('course_ids'):
        #    domain.append(('id', 'in', data.get('course_ids')))
        #if data.get('responsible_id'):
        #    domain.append(('responsible_id', '=', data.get('responsible_id')))

        sheet = workbook.add_worksheet('Plate Fuelboss Report')
        bold = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': '#fffbed', 'border': True})
        title = workbook.add_format({'bold': True, 'align': 'center', 'font_size': 20, 'bg_color': '#f2eee4', 'border': True})
        header_row_style = workbook.add_format({'bold': True, 'align': 'center', 'border': True})

        sheet.merge_range('A1:F1', 'Plate Report', title)

        employees = self.env['hr.employee'].search(domain)
        row = 3
        col = 0

        # Header row
        sheet.set_column(0, 5, 18)
        sheet.write(row, col, 'kolona 1', header_row_style)
        sheet.write(row, col+1, 'kolona 2', header_row_style)
        sheet.write(row, col+2, 'kolona 3', header_row_style)
        sheet.write(row, col+3, 'kolona 4', header_row_style)
        sheet.write(row, col+4, 'kolona 5', header_row_style)
        sheet.write(row, col+5, 'kolona 6', header_row_style)
        row += 2
        #for employee in employees:
        #    if employee.employee_ids:
        #        sheet.merge_range(f"A{row}:F{row}", employee.name, bold)
        #    for employee in employee.employee_ids:
        #        sheet.write(row, col, session.name)
        #        sheet.write(row, col+1, session.start_date)
        #        sheet.write(row, col+2, session.duration)
        #        sheet.write(row, col+3, session.seats)
        #        sheet.write(row, col+4, session.instructor_id.name)
        #        sheet.write(row, col+5, session.number_of_attendees())
        #        row += 1
        #    if course.session_ids:
        #        row += 1
