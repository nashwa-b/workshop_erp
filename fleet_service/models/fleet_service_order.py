# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.exceptions import ValidationError

class FleetServiceOrder(models.Model):
    """Fleet service"""
    _name = 'fleet.service.order'
    _description = 'Fleet Service Order'
    _inherit = ['mail.thread']

    name = fields.Char(readonly=True, default='New')
    vehicle_id = fields.Many2one('fleet.vehicle')
    technician_id = fields.Many2one('hr.employee')
    service_date = fields.Datetime(string='Date')
    state = fields.Selection([('draft', 'Draft'), ('confirmed', 'Confirmed'), ('in_progress', 'In Progress'), ('done', 'Done'),('cancelled', 'Cancelled')],
                             string='Status', default='draft')
    part_ids = fields.One2many('fleet.service.order.part', 'order_id', string='Part IDs')
    checklist_ids = fields.One2many('fleet.service.order.checklist', 'order_id',string='Checklist IDs')
    parts_total = fields.Float(string='Total Parts',compute ="_compute_parts_total",stored=True)
    labour_cost = fields.Float(string='Labour Cost')
    grand_total = fields.Float(string='Grand Total',compute="_compute_grand_total",store=True)
    checklist_progress = fields.Float(string='Checklist Progress', compute="_compute_checklist_progress",store=True)
    type_ids = fields.Many2many(
        'checklist.type',
    )


    @api.onchange('checklist_progress')
    def onchange_checklist_progress(self):
        if self.checklist_progress >= 100 and self.state == 'in_progress':
            self.state = 'done'

    def action_generate_ckecklist(self):
        for order in self:

            exist_types = order.mapped('type_ids.name')
            print(exist_types)
            print(order.checklist_ids)

            for i in exist_types:
                print("i",i)
                print("cehck",order.checklist_ids.mapped('task_name'))
                if i not in order.checklist_ids.mapped('task_name'):
                    order.checklist_ids = [fields.Command.create({
                        'task_name': i,
                    }) ]
                    print(order.checklist_ids)

                else:
                    raise ValidationError("Type Already Exists in Lines")


    def action_done(self):
        self.state = 'done'

    def action_cancel(self):
        self.state = 'cancelled'


    def action_confirm(self):
        """Raise validation error if order lines are not given"""
        if not self.part_ids:
            raise ValidationError("At least one part_ids line must exist")
        self.state = 'confirmed'

    def action_start_service(self):
        if not self.technician_id:
            raise ValidationError(" technician_id must be set")
        self.state = 'in_progress'





    @api.depends('checklist_ids')
    def _compute_checklist_progress(self):
        for order in self:
            if not order.checklist_ids:
                order.checklist_progress =0
            else:
                done_orders =  order.checklist_ids.filtered(lambda check: check.is_done == True)
                count = len(done_orders)
                print(count)
                count_checklist_items = len(order.checklist_ids)
                print(count_checklist_items)

                order.checklist_progress = (count / count_checklist_items)*100
                print(order.checklist_progress)



    @api.depends('parts_total','labour_cost')
    def _compute_grand_total(self):
        for record in self:
            record.grand_total = record.parts_total + record.labour_cost

    @api.depends('part_ids')
    def _compute_parts_total(self):
        for order in self:

            # order.parts_total = sum(self.part_ids.mapped('quantity'))
            total_qty = sum(self.part_ids.mapped('quantity'))
            total_unitprice= sum (self.part_ids.mapped('unit_price'))
            order.parts_total = total_qty*total_unitprice

            # record.total = sum(record.order_line_ids.mapped('sub_total'))




    @api.model_create_multi
    def create(self, vals_list):
        """Sequence Creation"""
        print(self)
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('fleet.service.order') or 'New'
        return super().create(vals)


