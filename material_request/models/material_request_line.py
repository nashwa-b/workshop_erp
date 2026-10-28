# -*- coding: utf-8 -*-

from odoo import fields, models,api


class MaterialRequestLine(models.Model):
    """Employee Loan Line"""
    _name = 'material.request.line'
    _description = 'Material Request Line'


    request_id = fields.Many2one('material.request', string='Request')
    product_id = fields.Many2one(
        'product.product','Product',
    )
    quantity = fields.Integer('Quantity',default = '1')
    uom_id = fields.Many2one('uom.uom', 'Unit')
    get_by = fields.Selection([('purchase_order', 'Purchase Order'),('internal_transfer', 'Internal Transfer')])


    sub_total = fields.Float(string="Sub Total", compute='_compute_sub_total', store=True)

    price_unit = fields.Float(
        string="Unit Price")

    source_location_id = fields.Many2one('stock.location', 'Source Location')
    destination_location_id = fields.Many2one('stock.location', 'Destination Location')
    picking_type_id = fields.Many2one(
        'stock.picking.type',
        string='Operation Type',
        domain=lambda self: [('code', '=', 'internal')])

    @api.onchange('product_id')
    def _onchange_product_id(self):
        """Unit Price"""
        if self.product_id:
            self.price_unit = self.product_id.list_price


    @api.depends('quantity', 'price_unit')
    def _compute_sub_total(self):
        """Sub Total"""
        for line in self:
            line.sub_total = line.quantity * line.price_unit
