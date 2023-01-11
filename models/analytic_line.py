from odoo import api, fields, models, _
from odoo.exceptions import ValidationError

class AccountAnalyticLineFB(models.Model):

    _inherit = 'account.analytic.line'
    _description = 'Analytic Line'

    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)

        #last_line = self.search([('journal_id', '=', defaults.get('journal_id'))], limit=1)
        #fields.Date.context_today(self)

        #self.env["account.analytic.line"].flush_model()
        #self.flush_model()

        #domain = [('write_uid', '=', self.env.context.get('uid'))] #+ (extra_domain or [])
        #order = "write_date desc"
        #last_line = self.env["account.analytic.line"].search(domain=domain, order=order, limit=1)

        #defaults['date'] = last_line.date
        #defaults['work_type_id'] = last_line.work_type_id
        #defaults['unit_amount'] = last_line.unit_amount


        return defaults
