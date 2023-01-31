from odoo import fields, models, api

class Task(models.Model):
    _name = "project.task"
    _inherit = "project.task"

    default_work_type_id = fields.Integer(compute='_default_work_type_id', store=False)
    default_date = fields.Date(compute='_default_date', store=False)
    default_unit_amount = fields.Float(compute='_default_unit_amount', store=False)

    #effective_hours_2 = fields.Float("Hours Spent 2", compute='_compute_effective_hours_2', compute_sudo=False, store=False)
    #@api.depends('timesheet_ids.unit_amount')
    #def _compute_effective_hours(self):
    #    if not any(self._ids):
    #        for task in self:
    #            task.effective_hours = round(sum(task.timesheet_ids.mapped('unit_amount')), 2)
    #        return

    #    #timesheet_read_group = self.env['account.analytic.line'].read_group([('task_id', 'in', self.ids)], ['unit_amount', 'task_id'], ['task_id'])
    #    #timesheets_per_task = {res['task_id'][0]: res['unit_amount'] for res in timesheet_read_group}
    #    #for task in self:
    #    #    task.effective_hours = round(timesheets_per_task.get(task.id, 0.0), 2)

    #def default_get(self, fields_list):
    #    defaults = super().default_get(fields_list)
    #
    #    #domain = [('write_uid', '=', self.env.context.get('uid'))] #+ (extra_domain or [])
    #    #order = "write_date desc"
    #    #last_line = self.env["account.analytic.line"].search(domain=domain, order=order, limit=1)
    #    #count = self.search_count([])

    #    #if self.env.context.get('default_date'):
    #    #defaults['date'] = last_line.date
    #    #defaults['work_type_id'] = last_line.work_type_id
    #    #defaults['unit_amount'] = last_line.unit_amount
    #    return defaults

    def get_default_value(self, field_name ):
        write_date = fields.Datetime.to_datetime('2022-01-01')
        value = None
        for timesheet in self.timesheet_ids:
            if timesheet.write_uid.id == self.env.context.get('uid') and timesheet.write_date:
                if timesheet.write_date > write_date:
                    write_date = timesheet.write_date
                    value = timesheet[field_name]
            else:
                # uncommited records
                # timesheet.id.ref = 'virtual_9', 'virtual_10' ...
                virtual_id = 0
                if not type(timesheet.id) is int:
                   if type(timesheet.id) is models.NewId:
                       if timesheet.id.ref:
                            new_virtual_id = int(timesheet.id.ref.replace('virtual_', ''))
                            if new_virtual_id > virtual_id:
                                virtual_id = new_virtual_id
                                value = timesheet[field_name]
        return value

    @api.depends('timesheet_ids.unit_amount', 'timesheet_ids.work_type_id', 'timesheet_ids.name', 'timesheet_ids.date',
                 'timesheet_ids.employee_id')
    def _default_work_type_id(self):
        self.default_work_type_id = self.get_default_value('work_type_id')
        return

    @api.depends('timesheet_ids.unit_amount', 'timesheet_ids.work_type_id', 'timesheet_ids.name', 'timesheet_ids.date',
                 'timesheet_ids.employee_id')
    def _default_date(self):
        self.default_date = self.get_default_value('date')
        return

    @api.depends('timesheet_ids.unit_amount', 'timesheet_ids.work_type_id', 'timesheet_ids.name', 'timesheet_ids.date',
                 'timesheet_ids.employee_id')
    def _default_unit_amount(self):
        self.default_unit_amount = self.get_default_value('unit_amount')
        return

