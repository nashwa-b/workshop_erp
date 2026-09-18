# -*- coding: utf-8 -*-

from odoo import fields, models


class ResUsers(models.Model):
    """Extend res user to create transfer request"""
    _inherit = 'res.users'

    approver_line_ids = fields.One2many('employee.transfer.wizard','company_id',string='Approve lines')

    def transfer_request(self):
        self.ensure_one()
        print(self)
        return {
            'type': 'ir.actions.act_window',
            'name': 'Employee Transfer',
            'res_model': 'employee.transfer.wizard',
            "views": [[self.env.ref('employee_transfer.view_employee_transfer_wizard_form').id, "form"]],
            'target': 'new',
            # 'context': {'default_product_id': self.id, 'default_price_unit': self.list_price}
        }


    def view_approval(self):
        self.ensure_one()
        print('w', self.id)
        print('l',self.user_id)
        return {
            'type': 'ir.actions.act_window',
            'name': 'Employee Transfer Approvals',
            'res_model': 'employee.transfer.wizard',
            'views': [[self.env.ref('employee_transfer.employee_transfers_view_list_button').id, "list"],[self.env.ref('employee_transfer.employee_transfer_view_form_button').id, "form"]],
            # "domain": [(self.user, '=', self.id)],
            'target': 'current'
        }



