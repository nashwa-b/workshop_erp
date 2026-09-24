# -*- coding: utf-8 -*-

from odoo import models, fields, api

from datetime import datetime

from odoo.exceptions import ValidationError



class WorkshopJobOrder(models.Model):
    """workshop job order"""
    _name = 'workshop.job.order'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Job Order'

    name = fields.Char(string='Number', required=True, readonly=True, default='New')
    customer_id = fields.Many2one('res.partner', string='Customer')
    # , related = 'vehicle_id.owner_id'
    phone = fields.Char(string='Phone Number', related='customer_id.phone')
    vehicle_id = fields.Many2one('workshop.vehicle', string='Vehicle', ondelete = 'restrict', required = True, domain = "[('owner_id', 'in', [customer_id])] if customer_id else []")
    mechanic_ids = fields.Many2many('hr.employee', string='Mechanics', tracking=True)
    job_type_id = fields.Many2one('job.type', string="Job Type")
    bay_id = fields.Many2one('workshop.bay', string='Workshop Bay', tracking = True)

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
    sale_order_id = fields.Many2one('sale.order', string='Sale Order')

    invoice_count = fields.Integer(string='Invoice Count', compute='_compute_invoice_count')
    invoice_paid = fields.Boolean(string='Invoice Paid', compute='_compute_invoice_paid')

    vehicle_image_ids = fields.One2many(
        string="Vehicle Images",
        comodel_name='product.image',
        inverse_name='job_order_id',
    )

    invoice_id = fields.Many2one('account.move', string='Invoice')


    hide = fields.Boolean(string="Hide", compute="_compute_hide", store=False)
    appointment_ids = fields.One2many("calendar.event", "job_order_id", string="Appointments")
    collected = fields.Boolean(string="Collected", default=False)
    # date_of_birth = fields.Date(string='Date of Birth')
    # age = fields.Float(string = 'Age',compute='_compute_age')

    # @api.depends('age')
    # def _compute_age(self):
    #     my_date = datetime.now()
    #     year = my_date.year

        # years = date_of_birth.year



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
        for record in self:
            # price_total = 0
            # order.amount_to_invoice = sum(order.order_line.mapped('amount_to_invoice'))
            record.total = sum(record.order_line_ids.mapped('sub_total'))

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
            self.bay_id.write({'status' : 'free', 'ongoing_job_id' : False})

        template = self.env.ref('workshop_erp.mail_template_job_order_done')
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
            'invoice_line_ids': [fields.Command.create({
                'product_id': line.product_id.id,
                'quantity': line.product_qty,
                'price_unit': line.price_unit,
                'price_subtotal': line.sub_total}) for line in self.order_line_ids],
        })
        invoice.action_post()
        self.write({'invoice_id': invoice.id, 'status': 'invoiced'})
        return self.action_view_invoice()

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

    def action_cancel(self):
        """workshop Bay Cancel"""
        if self.status == 'draft':
            self.status = 'cancel'
        else:
            raise ValidationError("Job orders in this state cannot be cancelled.")

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

    def _send_daily_remainder(self):
        """Send daily reminder until vehicle is collected"""
        rec = self.search([('invoice_id.payment_state','=','paid'), ('collected','=', False)])
        for record in rec:
            mail_template = self.env.ref('workshop_erp.mail_template_vehicle_pickup')
            email_values = {'email_to': record.customer_id.email}
            mail_template.send_mail(record.id, force_send=True, email_values=email_values)

    @api.onchange('vehicle_id')
    def onchange_vehicle_id(self):
        if self.vehicle_id:
            self.customer_id = self.vehicle_id.owner_id

    # def action_sale_order(self):
    #     customer=self.sale_order_id.partner_id.name
    #     print('1',customer)
    #     count = self.env['sale.order'].search_count([('partner_id', '=', customer)])
    #     print('2',count)
    #     total = self.env['sale.order'].search([('partner_id', '=', customer)])
    #     total_amount = sum(total.mapped('amount_total'))
    #     # total_amount = sum(total.mapped('price_total'))
    #     print('3',total_amount)
    #
    #     # invoice = self.env['account.move.line'].search([('move_id.partner_id',
    #     # '=', customer),('move_type','=','out_invoice')])
    #     # invoice_amount = sum(invoice.mapped('price_total'))
    #     # print('4',invoice_amount)
    #
    #     invoice = self.env['account.move'].search(
    #         [('partner_id', '=', customer), ('move_type', '=', 'out_invoice')])
    #     invoice_amount = sum(invoice.mapped('amount_total'))
    #     print('4', invoice_amount)
    #
    #     highest_amount = self.env['account.move'].search([('partner_id', '=', customer),('move_type','=','out_invoice')], order='amount_total desc' ,limit=1)
    #     # highest = highest_amount.move_id
    #     print('5',highest_amount.amount_total)
    #     print('5',highest_amount.name)
    #     # highest_amount = max(invoices)
    #     # print(highest_amount)
    #     lowest_amount = self.env['account.move'].search([('partner_id', '=', customer),('move_type','=','out_invoice')], order='amount_total asc' ,limit=1)
    #     # lowest = lowest_amount.move_id
    #     print('6',lowest_amount.amount_total)
    #     print('6',lowest_amount.name)
    #     purchase = self.env['sale.order.line'].search([('order_id.partner_id', '=', customer)])
    #     products = purchase.mapped('product_id.name')
    #     print('7',products)
    #     # purchases = self.env['sale.order.line'].search([('order_id.partner_id', '=', customer)])
    #     #
    #     # print("ii",purchases)
    #     purchase = self.env['sale.order.line'].search([('order_id.partner_id', '=', customer)], order='product_uom_qty desc',limit=1)
    #     # print(purchase)
    #     highest_prod = purchase.product_id.name
    #     print('8',highest_prod)
    #     purchase = self.env['sale.order.line'].search([('order_id.partner_id', '=', customer)], order='price_total desc',limit=1)
    #     purchase_amount=purchase.product_id.name
    #     print('9',purchase_amount)
    #
    #
    #
    #
    #


        # highest_amount = max(invoices)
        # print(highest_amount)
        # highest_number = self.env['account.move'].search([('price_total', '=',highest_amount)])
        # print(highest_number)




    class ProductImage(models.Model):
        """Add media of vehicles"""
        _inherit = 'product.image'
        job_order_id = fields.Many2one(string="Vehicle Images", comodel_name='workshop.job.order')
