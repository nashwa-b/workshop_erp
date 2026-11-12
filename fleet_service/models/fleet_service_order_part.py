# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.exceptions import ValidationError

class FleetServiceOrderPart(models.Model):
    """Employee Loan"""
    _name = 'fleet.service.order.part'
    _description = 'Fleet Service Order Part'

    order_id = fields.Many2one('fleet.service.order')
    product_id = fields.Many2one('product.product')
    quantity = fields.Float(string="Quantity")
    unit_price = fields.Float(string="Unit Price")

    @api.onchange('product_id')
    def _onchange_product_id(self):
        """Unit Price"""
        if self.product_id:
            self.unit_price = self.product_id.list_price

    # def _compute_unit_price(self):
    #     pass
    #
    # def _compute_quantity(self):
    #     pass

