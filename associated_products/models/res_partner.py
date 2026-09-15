# -*- coding: utf-8 -*-

from odoo import fields, models


class ResPartner(models.Model):
    """Extends partner model by adding smart buttons for vehicles and job orders associated with that partner"""
    _inherit = 'res.partner'

    associated_product_ids = fields.Many2many('product.product', string='Products')


