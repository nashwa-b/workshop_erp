# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.exceptions import UserError


class MaterialRequest(models.Model):
    """Material Request"""
    _name = 'material.request'
    _description = 'Material Request'
    _inherit = ['mail.thread']

    name = fields.Char('Name', readonly=True, default='New')
    date = fields.Date('Date of Request', default=fields.Date.context_today)
    requested_by = fields.Many2one(
        'res.users', 'Requested By', default=lambda self: self.env.user ,required = True)

    # requisition_department_manager_id = fields.Many2one('res.users','Department Manager',required=True)
    # requisition_head_id = fields.Many2one('res.users','Requisition Head',required=True)
    state = fields.Selection([('draft','Draft'),('manager_approval','Manager Approval'),('head_approval','Head Approval'),('request_order','Request Order'),('reject','Rejected')],string='Status',default = 'draft')
    source_location_id = fields.Many2one('stock.location','Source Location')
    transfer_count = fields.Integer(compute='_compute_transfer_count')
    purchase_count = fields.Integer(compute='_compute_purchase_count')
    request_line_ids = fields.One2many('material.request.line', 'request_id')

    def _compute_transfer_count(self):
        """compute transfer count"""
        for record in self:
            transfers = self.env['stock.picking'].search([('material_request_id', '=', self.id)])
            record.transfer_count = len(transfers)


    def _compute_purchase_count(self):
        for record in self:
            purchases = self.env['purchase.order'].search([('material_request_id','=',self.id)])
            record.purchase_count = len(purchases)


    def action_view_purchase(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "purchase.order",
            "name": "Purchase Order",
            "views": [[self.env.ref("purchase.purchase_order_kpis_tree").id, "list"]],
            "domain": [('material_request_id', '=', self.id)],
            "context": {'create': False}
        }
    def action_view_internal_transfer(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "stock.picking",
            "name": "Internal Transfers",
            "views": [[self.env.ref("stock.vpicktree").id, "list"]],
            "domain": [('material_request_id', '=', self.id)],
            "context": {'create': False}
        }


    def action_head_approval(self):
        # if self.env.user != self.requisition_head_id:
        #     raise UserError("Only Requisition Head can Approve the Request.")
        # else:
            self.state = 'request_order'
            for order in self:
                for line in order.request_line_ids:
                    product = line.product_id
                    print("l", product)
                    vendor_id = product.seller_ids[:1]
                    vendor = vendor_id.partner_id
                    print("Srf", order, order.id)
                    if line.get_by == 'purchase_order':
                        # product = line.product_id
                        # print("l", product)
                        # vendor_id = product.seller_ids[:1]
                        # vendor = vendor_id.partner_id
                        # print("Srf", order, order.id)
                        self.env['purchase.order'].create({
                            'partner_id': vendor.id,
                            'material_request_id': order.id,
                            'order_line': [fields.Command.create({
                                'product_id': product.id,
                                'product_qty': line.quantity,
                                'product_uom_id': line.uom_id.id,

                                'price_unit': line.price_unit,
                                'price_subtotal': line.sub_total,
                                # 'sale_line_id': line.id,
                            })],
                        })
                    if line.get_by == 'internal_transfer':
                        self.env['stock.picking'].create({
                            'partner_id': order.requested_by.partner_id.id,
                            # 'picking_type_id': self.env['stock.picking.type'].search([
                            #     ('code', '=', 'internal'),('default_location_src_id','=',order.source_location_id.id),('default_location_dest_id','=',order.destination_location_id.id)
                            # ], limit=1).id,
                            'material_request_id': order.id,
                            'move_ids': [fields.Command.create({
                                'product_id': product.id,
                                'product_uom_qty': line.quantity,
                                'product_uom': line.uom_id.id,
                                'location_id': order.source_location_id.id,
                                'location_dest_id': order.destination_location_id.id,
                                'picking_type_id': order.picking_type_id.id,

                                # 'price_unit': line.price_unit,
                                # 'price_subtotal': line.price_subtotal,
                                # 'sale_line_id': line.id,
                            })],
                        })



    def action_reject(self):
        # if self.env.user != self.requisition_head_id:
        #     raise UserError("Only Requisition Head can Reject the Request.")
        # else:
            self.state = 'reject'


    def action_manager_approval(self):
        # if self.env.user != self.requisition_department_manager_id:
        #     raise UserError("Only department manager can approve the request")
        # else:
            self.state = 'head_approval'

    def action_confirm(self):
        # if not self.request_line_ids:
        #     raise UserError("You cannot confirm the Job Order without Job Lines.")
        self.state = 'manager_approval'
        print(self.env.user)

    @api.model_create_multi
    def create(self, vals_list):
        """Sequence Creation"""
        print(self)
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('material.request') or 'New'
        return super().create(vals)
