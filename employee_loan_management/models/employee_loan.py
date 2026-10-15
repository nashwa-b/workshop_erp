# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.exceptions import ValidationError


class EmployeeLoan(models.Model):
    """Employee Loan"""
    _name = 'employee.loan'
    _description = 'Employee Loan'
    _inherit = ['mail.thread']

    name = fields.Char('Name',readonly=True, default='New')
    employee_id = fields.Many2one('hr.employee',string = 'Employee',required=True)
    loan_amount = fields.Float(string='Loan Amount')
    installment_count = fields.Integer(string='Installment Count', default=1)
    start_date = fields.Datetime(string='Start Date')
    state = fields.Selection([('draft','Draft'),('approved','Approved'),('ongoing','Ongoing'),('paid','Paid')], string='Status', default='draft')
    loan_line_ids = fields.One2many('employee.loan.line', inverse_name ="loan_id" ,string='Loan Lines')
    installment_amount = fields.Float(string='Installment Amount')
    total_payable = fields.Float(string='Total Payable', compute='_compute_total_payable')
    loan_line_count = fields.Integer(string='Loan Line Count', compute='_compute_loan_line_count', store=True)
    # total_payable = fields.Float(string='Total Payable')

    @api.depends('loan_line_ids')
    def _compute_loan_line_count(self):
        """Compute the number of Job Order for a vehicle"""
        for record in self:
            record.loan_line_count = len(record.loan_line_ids)

    def action_view_installments(self):
        """Open the vehicle view for this partner in smart button"""
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "employee.loan.line",
            "name": "Installments",
            "views": [[self.env.ref("employee_loan_management.employee_loan_line_view_list").id, "list"]],
            "domain": [('loan_id', '=', self.id)],
        }

    def action_approve_loan(self):
        if self.loan_amount  <= 0:
            raise ValidationError("Loan Amount Must Be Greater Than Zero")
        if self.installment_amount <= 0:
            raise ValidationError("Installment Amount Must Be Greater Than Zero")
        self.state = 'approved'

    def action_generate_installments(self):
        print("p",self)

        if self.installment_count:
            self.loan_line_ids = [fields.Command.create({
                'amount': self.installment_amount,
            }) for i in range(self.installment_count)]

            self.state = 'ongoing'

    def action_pay_installments(self):
        for record in self:
            for line in record.loan_line_ids:
                line.unlink()
        # self.state = 'paid'

    @api.depends('loan_amount')
    def _compute_total_payable(self):
        for record in self:
            record.total_payable = record.loan_amount

    @api.onchange('loan_amount','installment_count')
    def _onchange_loan_amount(self):
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
