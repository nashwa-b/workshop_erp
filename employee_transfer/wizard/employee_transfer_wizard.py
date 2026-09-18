# -*- coding: utf-8 -*-

from odoo import fields, models


class EmployeeTransferWizard(models.TransientModel):
    """Creation of Wizards for Sales Orders"""
    _name = 'employee.transfer.wizard'
    _description = 'Wizard for Employee Transfer'

    company_id = fields.Many2one('res.company', string="Choose Company")
    # user_id = fields.Many2one(
    #     "res.users",
    #     "Recruiter",
    #     default=lambda self: self.env.user)
    # quantity = fields.Float(string="Quantity", default=1)
    # price_unit = fields.Float(string="Unit Price")
    # product_id = fields.Many2one('product.product', string="Product")

    def button_approval(self):
        # print('i', self.partner_id.id)
        pass
        # manager = self.env.user.has_group('workshop_erp.group_workshop_job_order_manager')
        # if manager:
        #     # Reset approver lines
        #     new_lines = []
        #     for line in self.partner_id.approver_line_ids:
        #         # Place manager first
        #         # seq = 1 if line.user_id.id == manager.id else line.sequence + 1
        #         new_lines.create({
        #             'user_id': line.user_id.id,
        #             # 'sequence': seq,
        #             'company_id': line.company_id.id,
        #             'action': line.action
        #         })
        #     new = self.env['res.users'].create({'approver_line_ids': self.new_lines.id})
        #     print('j',new)
        # return new
            # approver_line_ids = new_lines

        # ApproverSudo = self.env['approval.approver'].sudo()
        # employee = self.env.user_id
        # manager = employee.parent_id.user_id
        #
        # approver_list = (manager, True, 10)
        # for user in approver_list:
        #     if user:
        #         ApproverSudo.create({
        #             'request_id': self.id,
        #             'user_id': user.id,
        #             # 'required': required,
        #             # 'sequence': seq,
        #             'status': 'new',
        #         })

    def button_approve(self, force=False):
        # self = self.filtered(lambda order: order._approval_allowed())
        new = self.env['res.users'].write({'company_id' : self.company_id.id})
        return new
        # self.filtered(lambda p: p.lock_confirmed_po == 'lock').write({'locked': True})
        # return {}

    # def _approval_allowed(self):
    #     """Returns whether the order qualifies to be approved by the current user"""
    #     self.ensure_one()
    #     return (
    #             # self.company_id.po_double_validation == 'one_step'
    #             # or (self.company_id.po_double_validation == 'two_step'
    #             #     and self.amount_total < self.env.company.currency_id._convert(
    #             #     self.company_id.po_double_validation_amount, self.currency_id, self.company_id,
    #             #     self.date_order or fields.Date.today()))
    #             self.env.user.has_group('workshop_erp.group_workshop_job_order_manager'))
    #
