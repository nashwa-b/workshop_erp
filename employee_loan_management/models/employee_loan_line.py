# -*- coding: utf-8 -*-

from odoo import fields, models


class EmployeeLoanLine(models.Model):
    """Employee Loan Line"""
    _name = 'employee.loan.line'
    _description = 'Employee Loan Line'

    loan_id = fields.Many2one('employee.loan',string='Loan')
    date = fields.Datetime(string='Date of Loan')
    amount = fields.Float(string='Amount')
    paid = fields.Boolean(string='Paid')



