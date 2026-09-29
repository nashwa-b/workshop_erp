# -*- coding: utf-8 -*-

from odoo import fields, models


class ResPartner(models.Model):
    """Adding associated products of the partner"""
    _inherit = 'res.partner'

    associated_product_ids = fields.Many2many('product.product', string='Products')


