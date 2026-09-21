# -*- coding: utf-8 -*-

from odoo import fields, models


class ResUsers(models.Model):
    """Extend res user to create transfer request"""
    _inherit = 'res.users'

    def action_transfer_request(self):
        """To show wizard"""
        self.ensure_one()
        print(self)
        return {
            'type': 'ir.actions.act_window',
            'name': 'Employee Transfer',
            'res_model': 'employee.transfer.wizard',
            "views": [[self.env.ref('employee_transfer.view_employee_transfer_wizard_form').id, "form"]],
            'target': 'new'
        }


    def action_view_approval(self):
        """To view user approval requests within smart button"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Employee Transfer Requests',
            'res_model': 'employee.transfer.request',
            'views': [[self.env.ref('employee_transfer.employee_transfer_request_view_list').id, "list"],[self.env.ref('employee_transfer.employee_transfer_request_view_form').id, "form"]],
            "domain": [('user_id', '=', self.id)],
            'target': 'current'
        }




# class HrEmployee(models.Model):
#     _inherit = "hr.employee"
#
#         def action_view_approval(self):
#             """To view user approval requests within smart button"""
#             self.ensure_one()
#             return {
#                 'type': 'ir.actions.act_window',
#                 'name': 'Employee Transfer Requests',
#                 'res_model': 'employee.transfer.request',
#                 'views': [[self.env.ref('employee_transfer.employee_transfer_request_view_list').id, "list"],[self.env.ref('employee_transfer.employee_transfer_request_view_form').id, "form"]],
#                 "domain": [('user_id', '=', self.id)],
#                 'target': 'current'
#             }





