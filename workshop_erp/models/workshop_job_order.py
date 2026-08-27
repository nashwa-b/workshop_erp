# -*- coding: utf-8 -*-

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
    quotation_count = fields.Integer(
        string='Vehicles',
        # compute='_compute_vehicle_count',
        help='Number of vehicle contracts for this partner'
    )

    sale_order_id = fields.Many2one(
        'sale.order', 'Sale Order', check_company=True, readonly=True, index='btree_not_null',
        copy=False, help="Sale Order from which the Repair Order comes from.")
    sale_order_line_id = fields.Many2one(
        'sale.order.line', check_company=True, readonly=True,
        copy=False, help="Sale Order Line from which the Repair Order comes from.")

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
        # print(self)
        for order in self:
            # print(order.order_line)
            price_total = 0
            for line in order.order_line_ids:
                # print("line",line.sub_total)
                price_total += line.sub_total

            order.total = price_total

    def action_create_sale_order(self):
        self._create_sale_order()
        return self.action_view_sale_order()

    def action_view_sale_order(self):
        return {
            "type": "ir.actions.act_window",
            "res_model": "sale.order",
            "views": [[False, "form"]],
            "res_id": self.sale_order_id.id
        }

    def _create_repair_sale_order_line(self):
        if not self:
            return
        so_line_vals = []
        for move in self:
            if move.sale_order_line_id or not move.order_id.sale_order_id:
                continue
            # so_line_vals.append(move._prepare_repair_so_line_vals())

        self.env['sale.order.line'].create(so_line_vals)

    #
    def _get_sale_order_values(self):
        print(self)
        # self.ensure_one()

        return {
            # "company_id": self.company_id.id,
            "partner_id": self.customer_id.id,

            "vehicle_id": self.vehicle_id.id,
            # "warehouse_id": self.picking_type_id.warehouse_id.id,
            # "order_line_ids": [Command.link(self.id)],
            "origin": self.name,
        }


        rslt = self.env['workshop.job.order'].create({
        'order_line_ids': [(0, 0, {
        #         # 'name': 'test line',
        #         # 'origin': self.name,
        #         # 'account_id': self.account_income.id,
                'price_unit': self.price_unit,
                # 'product_qty': 1.0,
        #         # 'discount': 0.0,
        #         # 'uom_id': product.uom_id.id,
                'product_id': self.product_id.id,
        #         # 'sale_line_ids': [(6, 0, [line.id for line in sale_order_id.order_line])],
            })],
        })

        new_sale_order = self.env['sale.order'].create(rslt)

        return {
            'type': 'ir.actions.act_window',
            'name': 'Sales Order',
            'res_model': 'sale.order',
            'res_id': new_sale_order.id,
            'view_mode': 'form',
            'target': 'current',
        }

        # rslt = self.env['workshop.job.order'].create({
        #     'customer_id': self.customer_id.id,
        #     'vehicle_id': self.vehicle_id.id,
        #     # 'name': 'customer invoice',
        #     # 'type': 'out_invoice',
        #     # 'date_invoice': date,
        #     # 'account_id': self.account_receivable.id,
        #     # 'order_line_ids': [(0, 0, {
        #         # 'name': 'test line',
        #         # 'origin': self.name,
        #         # 'account_id': self.account_income.id,
        #         # 'price_unit': self.price_unit,
        #         # 'product_qty': 1.0,
        #         # 'discount': 0.0,
        #         # 'uom_id': product.uom_id.id,
        #         # 'product_id': self.product_id.id,
        #         # 'sale_line_ids': [(6, 0, [line.id for line in sale_order_id.order_line])],
        #     # })],
        # })
        #
        # return rslt
        #
        #
        # return {
        #     "partner_id": self.customer_id.id,
        #     "job_order_id": self.name,
        #     "vehicle_id": self.vehicle_id.id,
        #     # "customer_id": self.customer_id.id,
        #     # "warehouse_id": self.picking_type_id.warehouse_id.id,
        #     # "order_line_ids": [Command.link(self.id)],
        #     "origin": self.name
        # }

    #     order_lines = []
    #     if self.order_line_ids:
    #         order_lines.append( {
    #             'product_id': self.order_line_ids.id,
    #         'product_qty': self.order_line_ids,
    #         'price_unit': self.order_line_ids
    #     })
    #
    #     sale_order_vals = {
    #     'partner_id': self.customer_id.id,
    #     'order_line': order_lines,
    #     'origin': self.name
    # }

    # new_sale_order = self.env['sale.order'].create(sale_order_vals)
    #


    def _create_sale_order(self):
        # print(self)

        if any(order.sale_order_id for order in self):
            concerned_ro = self.filtered('sale_order_id')
            ref_str = "\n".join(jo.name for jo in concerned_ro)
            raise UserError(
                _(
                    "You cannot create a quotation for a repair order that is already linked to an existing sale order.\nConcerned repair order(s):\n%(ref_str)s",
                    ref_str=ref_str,
                ),
            )

        if any(not order.customer_id for order in self):
            concerned_ro = self.filtered(lambda ro: not ro.partner_id)
            ref_str = "\n".join(jo.name for jo in concerned_ro)
            raise UserError(
                _(
                    "You need to define a customer for a repair order in order to create an associated quotation.\nConcerned repair order(s):\n%(ref_str)s",
                    ref_str=ref_str,
                ),
            )

        sale_order_values_list = [order._get_sale_order_values() for order in self]
        sale_orders = self.env['sale.order'].create(sale_order_values_list)
        # Add Sale Order Lines for 'add' move_ids
        # self.order_line_ids._create_repair_sale_order_line()
        return sale_orders
