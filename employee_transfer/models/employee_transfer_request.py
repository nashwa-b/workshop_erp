# -*- coding: utf-8 -*-

from odoo import fields, models


class EmployeeTransferRequest(models.Model):
    """workshop job types"""
    _name = 'employee.transfer.request'
    _description = 'Transfer Request'
    _inherit = ['mail.thread']

    current_company_id = fields.Many2one('res.company')
    company_id = fields.Many2one('res.company',string='Company to change', tracking=True)
    user_id = fields.Many2one('res.users',string='User')
    state = fields.Selection([("approved", "Approved"), ("rejected", "Rejected")], tracking=True)

    def action_button_approve(self):
        """Button to change to the company requested by user"""
        print(self.company_id.id)
        self.user_id.write({'company_id': self.company_id.id})
        self.state = 'approved'

    def action_button_reject(self):
        """Change state to rejected"""
        self.state = 'rejected'
