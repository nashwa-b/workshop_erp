# -*- coding: utf-8 -*-

from odoo import models, fields, api

from datetime import datetime

from odoo import models, fields
from odoo.exceptions import ValidationError


class WorkshopJobOrder(models.Model):
    """workshop job order"""
    _name = 'workshop.job.order'
    _inherit = ['mail.thread']
    _description = 'Job Order'

    name = fields.Char(string='Number', required=True, copy=False, readonly=True, default='New')
    customer_id = fields.Many2one('res.partner', string='Customer')
    phone = fields.Char(string='Phone Number', related='customer_id.phone')
    vehicle_id = fields.Many2one('workshop.vehicle', string='Vehicle', ondelete='restrict', required=True)
    mechanic_ids = fields.Many2many('hr.employee', string='Mechanics', tracking=True)
    bay_id = fields.Many2one('workshop.bay', string='Workshop Bay', tracking=True)
    job_date = fields.Date(string='Job Date', default=datetime.today())
    customer_note = fields.Text(string='Customer Note')
    image = fields.Image(string='Image')
    total = fields.Float(string='Total', compute='_compute_total', store=True)
    status = fields.Selection(
        [("draft", "Draft"), ("confirmed", "Confirmed"), ("in_progress", "In Progress"), ("done", "Done"),
         ("invoiced", "Invoiced"), ("cancel", "Cancelled")], string='Status', default='draft', tracking=True)
    repair_instructions = fields.Html(string='Repair instructions')
    warranty = fields.Boolean(string="Under Warranty", default=False)
    order_line_ids = fields.One2many(
        comodel_name='workshop.job.line',
        inverse_name='order_id',
        string='Job Order Lines',
        copy=True, bypass_search_access=True)

    def action_confirm(self):
        """Workshop Bay Confirmation"""
        for record in self:
            if not record.order_line_ids:
                raise ValidationError("You cannot confirm the Job Order without Job Lines.")
            self.status = 'confirmed'

    def action_start(self):
        """Workshop Bay Start"""
        self.ensure_one()
        self.status = 'in_progress'
        for rec in self:
            if rec.bay_id:
                rec.bay_id.status = 'occupied'
                rec.bay_id.ongoing_job_id = rec.id
        return True

    def action_done(self):
        """Workshop Bay Done"""
        self.status = 'done'

    def action_invoiced(self):
        """Workshop Bay Invoiced"""
        self.status = 'invoiced'

    def action_cancel(self):
        """workshop Bay Cancel"""
        self.status = 'cancel'

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('workshop.job.order') or 'New'
        return super().create(vals)

    @api.depends('order_line_ids')
    def _compute_total(self):
        """Total Amount"""
        print(self)
        for order in self:
            # print(order.order_line)
            price_total=0
            for line in order.order_line_ids:
                print("line",line.sub_total)
                price_total += line.sub_total

            order.total = price_total






