# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.exceptions import ValidationError


class EmployeeLoan(models.Model):
    """Employee Loan"""
    _name = 'employee.loan'
    _description = 'Employee Loan'
    _inherit = ['mail.thread']

    name = fields.Char('Name', readonly=True, default='New')
    employee_id = fields.Many2one('hr.employee', string='Employee', required=True,
                                  domain="[('employee_id.loan_not_allowed', '==', False)]")
    loan_amount = fields.Float(string='Loan Amount')
    installment_count = fields.Integer(string='Installment Count', default=1)
    start_date = fields.Datetime(string='Start Date')
    state = fields.Selection([('draft', 'Draft'), ('approved', 'Approved'), ('ongoing', 'Ongoing'), ('paid', 'Paid')],
                             string='Status', default='draft')
    loan_line_ids = fields.One2many('employee.loan.line', inverse_name="loan_id", string='Loan Lines')
    installment_amount = fields.Float(string='Installment Amount')
    total_payable = fields.Float(string='Total Payable', compute='_compute_total_payable')
    loan_line_count = fields.Integer(string='Loan Line Count', compute='_compute_loan_line_count', store=True)
    paid_amount = fields.Float(string='Paid Amount', compute='_compute_paid_amount', store=True)
    balance_amount = fields.Float(string='Balance Amount', compute='_compute_balance_amount', store=True)

    def _compute_balance_amount(self):
        """Compute balance amount"""
        for record in self:
            record.balance_amount = record.total_payable - record.paid_amount

    @api.depends('loan_line_ids')
    def _compute_paid_amount(self):
        """Compute paid amount"""
        for record in self:
            for line in record.loan_line_ids:
                if line.paid:
                    record.paid_amount += line.amount

    @api.depends('loan_line_ids')
    def _compute_loan_line_count(self):
        """Compute loan line count"""
        """Compute the number of Job Order for a vehicle"""
        for record in self:
            record.loan_line_count = len(record.loan_line_ids)

    @api.depends('loan_amount')
    def _compute_total_payable(self):
        """Compute total payable"""
        for record in self:
            record.total_payable = record.loan_amount

    def action_view_installments(self):
        """Opens loan line ids of corresponding loan"""
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "employee.loan.line",
            "name": "Installments",
            "views": [[self.env.ref("employee_loan_management.employee_loan_line_view_list").id, "list"]],
            "domain": [('loan_id', '=', self.id)],
        }

    def action_approve_loan(self):
        """Raise validation error when loan amount or installment amounts are less than zero"""
        if self.loan_amount <= 0:
            raise ValidationError("Loan Amount Must Be Greater Than Zero")
        if self.installment_amount <= 0:
            raise ValidationError("Installment Amount Must Be Greater Than Zero")
        self.state = 'approved'

    def action_generate_installments(self):
        """generate loan line ids of according to installment count and change state to ongoing"""
        print("p", self)
        if self.installment_count:
            self.loan_line_ids = [fields.Command.create({
                'amount': self.installment_amount,
            }) for i in range(self.installment_count)]

            self.state = 'ongoing'

    def action_pay_installments(self):
        """make the first unpaid line as paid and if all the lines are paid,move it to paid state"""
        for record in self:
            line = record.loan_line_ids.filtered(lambda line: not line.paid)[:1]
            if line:
                line.paid = True
            lines = record.loan_line_ids
            if lines and all(lines.mapped('paid')):
                record.state = 'paid'

    @api.onchange('loan_amount', 'installment_count')
    def _onchange_loan_amount(self):
        """Compute installment amount on change of loan amount and installment count"""
        if self.installment_count == 0:
            self.installment_amount = 0
        else:
            self.installment_amount = self.loan_amount / self.installment_count

    @api.model_create_multi
    def create(self, vals_list):
        """Sequence Creation"""
        print(self)
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('employee.loan') or 'New'
        return super().create(vals)
