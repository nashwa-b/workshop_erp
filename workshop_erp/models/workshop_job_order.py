# -*- coding: utf-8 -*-

from odoo import models, fields, api

from datetime import datetime

from odoo import models, fields
from odoo.exceptions import ValidationError
from odoo.fields import Command


class WorkshopJobOrder(models.Model):
    """workshop job order"""
    _name = 'workshop.job.order'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Job Order'

    name = fields.Char(string='Number', required=True, check_company=True, readonly=True, default='New')
    customer_id = fields.Many2one('res.partner', string='Customer', related='vehicle_id.owner_id')
    phone = fields.Char(string='Phone Number', related='customer_id.phone')
    vehicle_id = fields.Many2one('workshop.vehicle', string='Vehicle', ondelete='restrict', required=True, domain="[('owner_id', 'in', [customer_id])] if customer_id else []")
    alternative_id = fields.Many2one('res.partner', string='Vehicle', ondelete='restrict', required=True)
    mechanic_ids = fields.Many2many('hr.employee', string='Mechanics', tracking=True)
    job_type_id = fields.Many2one('job.type', string="Job Type")
    bay_id = fields.Many2one('workshop.bay', string='Workshop Bay', tracking=True)
    job_date = fields.Date(string='Job Date', default=datetime.today())
    customer_note = fields.Text(string='Customer Note')
    total = fields.Float(string='Total', compute='_compute_total',  store=True)
    status = fields.Selection(
        [("draft", "Draft"), ("confirmed", "Confirmed"), ("in_progress", "In Progress"), ("done", "Done"),
         ("invoiced", "Invoiced"), ("cancel", "Cancelled")], string='Status', default='draft', tracking=True)
    repair_instructions = fields.Html('Repair Instructions')
    warranty = fields.Boolean(string="Under Warranty", default=False)
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)

    order_line_ids = fields.One2many(
        comodel_name='workshop.job.line',
        inverse_name='order_id',
        string='Job Order Lines')

    invoice_count = fields.Integer(string='Invoice Count', compute='_compute_invoice_count')
    invoice_paid = fields.Boolean(string='Invoice Paid', compute='_compute_invoice_paid')

    vehicle_image_ids = fields.One2many(
        string="Vehicle Images",
        comodel_name='product.image',
        inverse_name='job_order_id',
    )

    invoice_id = fields.Many2one('account.move', string='Invoice')
    sale_order_id = fields.Many2one(
        'sale.order', 'Sale Order')

    hide = fields.Boolean(string="Hide", compute="_compute_hide", store=False)

    @api.depends('job_type_id')
    def _compute_hide(self):
        """hiding create quotation button for washing job type"""
        for record in self:
            if record.job_type_id == self.env.ref('workshop_erp.job_type_washing'):
                record.hide = True
            else:
                record.hide = False

    def _compute_invoice_paid(self):
        """Adding paid ribbon in job order"""
        for record in self:
            record.invoice_paid = record.invoice_id.payment_state == 'paid'

    @api.depends('order_line_ids')
    def _compute_total(self):
        """Total Amount"""
        # print(order.order_line)
        price_total = 0
        for line in self.order_line_ids:
            # print("line",line.sub_total)
            price_total += line.sub_total

        self.total = price_total

    def _compute_invoice_count(self):
        """Computation of invoice count for smart button"""
        for record in self:
            record.invoice_count = len(record.invoice_id)

    def action_confirm(self):
        """Raise validation error if order lines are not given"""
        if not self.order_line_ids:
            raise ValidationError("You cannot confirm the Job Order without Job Lines.")
        self.status = 'confirmed'


    def action_start(self):
        """Workshop Bay Start"""
        self.ensure_one()
        self.status = 'in_progress'
        if self.bay_id:
            self.bay_id.write({'status' : 'occupied', 'ongoing_job_id' : self.id})


    def action_done(self):
        """Job order status to done, automatic mail and follow-up activity"""
        self.status = 'done'
        if self.bay_id:
            self.bay_id.write({'status' : 'free', 'ongoing_job_id' : 0})

        template = self.env.ref('workshop_erp.mail_template_job_order')
        email_values = {'email_to': self.customer_id.email}
        template.send_mail(self.id, force_send=True, email_values=email_values)

        activity_type = self.env.ref('mail.mail_activity_data_call')
        self.env['mail.activity'].create({
            'activity_type_id': activity_type.id,
            'res_model_id': self.env['ir.model']._get_id('workshop.job.order'),
            'res_id': self.id,
            'user_id': self.env.user.id,
            # 'user_id': self.env.ref('workshop_erp.group_workshop_job_order_receptionist').user_ids.id,
            'date_deadline': fields.Date.today(),
            'summary': 'Call Customer',
        })


    def action_invoiced(self):
        """invoice button for washing job type"""
        self.ensure_one()
        invoice = self.env['account.move'].create({
            'move_type': 'out_invoice',
            'partner_id': self.customer_id.id,
            'invoice_line_ids': [Command.create({
                'product_id': line.product_id.id,
                'quantity': line.product_qty,
                'price_unit': line.price_unit,
                'price_subtotal': line.sub_total}) for line in self.order_line_ids],
        })
        invoice.action_post()
        self.write({'invoice_id': invoice.id, 'status': 'invoiced'})
        return self.action_view_invoice()


    def action_cancel(self):
        """workshop Bay Cancel"""
        if self.status == 'draft':
            self.status = 'cancel'


    @api.model_create_multi
    def create(self, vals_list):
        """Sequence Creation"""
        print(self)
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('workshop.job.order') or 'New'
        return super().create(vals)


    def _get_sale_order_values(self):
        """sale order values"""
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
        """View Sale Order Creation"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Quotation',
            'res_id': self.sale_order_id.id,
            'res_model': 'sale.order',
            "views": [[False, "form"]],
            'target': 'current'
        }

    def action_view_invoice(self):
        """Invoice View in Smart Button"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoice',
            'res_model': 'account.move',
            "views": [[False, "form"]],
            'res_id': self.invoice_id.id,
            'target': 'current'
        }



    class ProductImage(models.Model):
        """Add Media"""
        _inherit = 'product.image'

        job_order_id = fields.Many2one(
            string="Product Template", comodel_name='workshop.job.order', ondelete='cascade', index=True,
        )
