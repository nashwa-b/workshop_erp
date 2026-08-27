# -*- coding: utf-8 -*-

from odoo import fields, models, api

from odoo import models, fields
from odoo.fields import Command


class WorkshopJobLine(models.Model):
    """ Workshop Bay """
    _name = 'workshop.job.line'
    _description = 'Job Lines'

    order_id = fields.Many2one(
        comodel_name='workshop.job.order',
        string='Order Reference',
        ondelete='cascade'
    )

    product_id = fields.Many2one(
        comodel_name='product.product',
        string="Product",
        check_company=True)

    product_qty = fields.Float(
        string="Quantity",
        digits='Product Unit')

    sub_total = fields.Float(string="Sub Total", compute='_compute_sub_total')

    price_unit = fields.Float(
        string="Unit Price")

    @api.onchange('product_id')
    def _onchange_product_id(self):
        """Unit Price"""
        if self.product_id:
            self.price_unit = self.product_id.list_price
        else:
            self.price_unit = 0.0

    @api.depends('product_qty', 'price_unit')
    def _compute_sub_total(self):
        """Sub Total"""
        for line in self:
            line.sub_total = line.product_qty * line.price_unit

    def _prepare_repair_so_line_vals(self):
        self.ensure_one()
        product_qty = self.product_qty if self.order_id.status != 'done' else self.quantity
        vals = {
            'order_id': self.order_id.sale_order_id.id,
            'product_id': self.product_id.id,
            'product_uom_qty': product_qty,
            # When relying only on so_line compute method, the sol quantity is only updated on next sol creation
            # 'product_uom_id': self.product.id,
            'move_ids': [Command.link(self.id)],
            # 'qty_delivered': self.quantity if self.state == 'done' else 0.0,
        }
        if self.order_id.under_warranty:
            vals['price_unit'] = 0.0
        elif self.price_unit:
            vals['price_unit'] = self.price_unit
        return vals

    def _create_repair_sale_order_line(self):
        if not self:
            return
        so_line_vals = []
        for move in self:
            if not move.order_id.sale_order_id:
                continue
            so_line_vals.append(move._prepare_repair_so_line_vals())
        self.env['sale.order.line'].create(so_line_vals)

    # def _get_sale_order_values(self):
    #     self.ensure_one()
    #
    #     order_lines = []
    #     if self.product_id:
    #         order_lines.append( {
    #             'product_id': self.product_id.id,
    #             'product_qty': self.product_qty.id,
    #             'price_unit': self.price_unit.list_price,
    #         })
    #
    #     sale_order_vals = {
    #         'partner_id': self.customer_id.id,
    #         'order_line': order_lines,
    #         'origin': self.name
    #     }
    #
    #     new_sale_order = self.env['sale.order'].create(sale_order_vals)
    #
    #     return {
    #         'type': 'ir.actions.act_window',
    #         'name': 'Sales Order',
    #         'res_model': 'sale.order',
    #         'res_id': new_sale_order.id,
    #         'view_mode': 'form',
    #         'target': 'current',
    #     }
    #
    #
    #
    #
    #
    #
