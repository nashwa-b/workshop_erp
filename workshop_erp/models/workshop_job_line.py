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
        digits='Product Unit', default=1)

    sub_total = fields.Float(string="Sub Total", compute='_compute_sub_total')

    price_unit = fields.Float(
        string="Unit Price")


    @api.onchange('product_id')
    def _onchange_product_id(self):
        """Unit Price"""
        if self.product_id:
            self.price_unit = self.product_id.list_price


    @api.depends('product_qty', 'price_unit')
    def _compute_sub_total(self):
        """Sub Total"""
        for line in self:
            line.sub_total = line.product_qty * line.price_unit

