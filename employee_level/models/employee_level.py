# -*- coding: utf-8 -*-

from odoo import fields, models, api


class EmployeeLevel(models.Model):
    """ Model to add level and salary of employee """
    _name = 'employee.level'
    _description = 'Employee Level'
    _rec_name = 'level'

    level = fields.Integer(string="Level")
    salary = fields.Float("Salary")
    is_max_level = fields.Boolean(string="Is Max Level", compute="_compute_is_max_level", default=False, store=True)


    @api.ondelete(at_uninstall=False)
    def _compute_is_max_level(self):
        records = self.env['employee.level'].search([('is_max_level','=',True)])
        records.write({'is_max_level': False})
        max_level = self.env['employee.level'].search([], order='level desc', limit=1)
        print(max_level.is_max_level)
        for record in self:
            if record.level == max_level.level:
                record.is_max_level = True
                print(record.is_max_level)
        # for record in self:
        #     record.is_max_level = False
        #     if record.level == max_level.level:
        #         record.is_max_level = True
        #
        #         print(record.is_max_level)
