# -*- coding: utf-8 -*-
from itertools import count

from reportlab.graphics.transform import inverse

from odoo import models, fields, api

from datetime import datetime

from odoo import models, fields
from odoo.exceptions import ValidationError
from odoo.fields import Command


class WorkshopJobOrder(models.Model):
    """workshop job order"""
    _name = 'workshop.job.order'
    _inherit = ['mail.thread']
    _description = 'Job Order'

    name = fields.Char(string='Number', required=True, copy=False, readonly=True, default='New')
    customer_id = fields.Many2one('res.partner', string='Customer')
    phone = fields.Char(string='Phone Number', related='customer_id.phone')
    vehicle_id = fields.Many2one('workshop.vehicle', string='Vehicle', ondelete='restrict')
    mechanic_ids = fields.Many2many('hr.employee', string='Mechanics', tracking=True)
    user_id = fields.Many2one('res.users', string='Customer')
    bay_id = fields.Many2one('workshop.bay', string='Workshop Bay', tracking=True)
    job_date = fields.Date(string='Job Date', default=datetime.today())
    customer_note = fields.Text(string='Customer Note')
    image = fields.Image(string='Image')
    total = fields.Float(string='Total', compute='_compute_total', store=True)
    status = fields.Selection(
        [("draft", "Draft"), ("confirmed", "Confirmed"), ("in_progress", "In Progress"), ("done", "Done"),
         ("invoiced", "Invoiced"), ("cancel", "Cancelled")], string='Status', default='draft', tracking=True)
    repair_instructions = fields.Html('Repair Instructions')
    warranty = fields.Boolean(string="Under Warranty", default=False)
    # job_card_id = fields.Many2one('account.move', string='Job Card')
    job_order_id = fields.Many2one('account.move', string='Job Order')

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)

    order_line_ids = fields.One2many(
        comodel_name='workshop.job.line',
        inverse_name='order_id',
        string='Job Order Lines', )
    invoice_count = fields.Integer(string='Invoice Count', compute='_compute_invoice_count')

    product_template_image_ids = fields.One2many(
        string="Extra Product Media",
        comodel_name='workshop.media',
        inverse_name='product_tmpl_id',
    )

    product_tmpl_id = fields.Many2one(
        string="Product Template", comodel_name='workshop.media', ondelete='cascade', index=True,
    )

    invoice_id = fields.Many2one('account.move', string='Invoice')
    sale_order_id = fields.Many2one(
        'sale.order', 'Sale Order', check_company=True, readonly=True, index='btree_not_null',
        copy=False, help="Sale Order from which the Job Order comes from.")

    sale_order_line_id = fields.Many2one(
        'sale.order.line', check_company=True, readonly=True,
        copy=False, help="Sale Order Line from which the Job Order comes from.")

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

    #
    # def action_invoiced(self):
    #     """Workshop Bay Invoiced"""
    #     self.ensure_one()
    #     # self.status = 'invoiced'
    #
    #     for line in self.order_line_ids:
    #         # print(self.customer_id.name)
    #         invoice = self.env['account.move'].create({
    #             'move_type': 'out_invoice',
    #             'partner_id': self.customer_id.id,
    #             'invoice_line_ids': [
    #                 Command.create(
    #                     {'product_id': line.product_id.id, 'quantity': line.product_qty, 'price_unit': line.price_unit,
    #                      'price_subtotal': line.sub_total})
    #             ],
    #         })
    #         self.invoice_id = invoice.id

    #         print(self.invoice_id)
    #         print(invoice)
    #         print(line.product_id.name)


    def action_cancel(self):
        """workshop Bay Cancel"""
        self.status = 'cancel'

    @api.model_create_multi
    def create(self, vals_list):
        """Sequence Creation"""
        print(self)
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('workshop.job.order') or 'New'
        return super().create(vals)

    @api.depends('order_line_ids')
    def _compute_total(self):
        """Total Amount"""
        # print(self)
        for order in self:
            # print(order.order_line)
            price_total = 0
            for line in order.order_line_ids:
                # print("line",line.sub_total)
                price_total += line.sub_total

            order.total = price_total

    def _get_sale_order_values(self):
        return {
            'partner_id': self.customer_id.id,
            'job_order_id': self.id,
            'vehicle_id': self.vehicle_id.id,
            'origin': self.name,
        }

    def action_create_sale_order(self):
        """Sale Order Creation"""
        self.ensure_one()

        if self.sale_order_id:
            return self.action_view_sale_order()

        sale_order = self.env['sale.order'].create(
            self._get_sale_order_values()
        )

        for line in self.order_line_ids:
            self.env['sale.order.line'].create({
                'order_id': sale_order.id,
                'product_id': line.product_id.id,
                'product_uom_qty': line.product_qty,
                'price_unit': line.price_unit,
            })

        self.sale_order_id = sale_order.id

        return self.action_view_sale_order()

    def action_view_sale_order(self):
        self.ensure_one()

        return {
            'type': 'ir.actions.act_window',
            'name': 'Quotation',
            'res_model': 'sale.order',
            "views": [[False, "form"]],
            'res_id': self.sale_order_id.id,
            'target': 'current'
        }


    def action_view_invoice(self):
        """Invoice View"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoice',
            'res_model': 'account.move',
            "views": [[False, "form"]],
            'res_id': self.invoice_id.id,
            'target': 'current'
        }

    def _compute_invoice_count(self):
        self.invoice_count = len(self.invoice_id)
        # print(self.invoice_count)
        # self.invoice_count = 1 if self.invoice_id else 0


class AddMedia(models.Model):
    _name = 'workshop.media'

    product_tmpl_id = fields.Many2one(
        string="Product Template", comodel_name='workshop.job.order', ondelete='cascade', index=True,
    )
