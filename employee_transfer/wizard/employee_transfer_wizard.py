# -*- coding: utf-8 -*-

from odoo import fields, models


class EmployeeTransferWizard(models.TransientModel):
    """Creation of Wizard for employee transfer"""
    _name = 'employee.transfer.wizard'
    _description = 'Wizard for Employee Transfer'

    company_id = fields.Many2one('res.company', string="Choose Company")
    user_id = fields.Many2one(
        "res.users",
        "User",
        default=lambda self: self.env.user)

    def action_button_send_approval(self):
        """Create records during approval request"""
        self.env['employee.transfer.request'].create({
            'user_id': self.user_id.id,
            'company_id': self.company_id.id,
            'current_company_id': self.user_id.company_id.id,
        })
