from odoo import models, fields, api, _
from odoo.exceptions import UserError


class EmployeeReport(models.AbstractModel):
    _name = 'report.payroll.fuelboss.report_employee_view'

    @api.model
    def _get_report_values(self, docids, data=None):
        #if not self.env.user.has_group('openacademy.group_manager_openacademy'):
        #    raise UserError('You do not have access to print this report!')

        # sessions = self.env['openacademy.session'].browse(docids)
        # for session in sessions:
        #     if len(session.attendee_ids) == 0:
        #         raise UserError(f"{session.display_name} have no attendees!")
        return {
            'doc_ids': docids,
            'doc_model': 'hr.employee',
            'docs': self.env['hr.employee'].browse(docids),
        }