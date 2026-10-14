# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ProductBrand(models.Model):
    """Extends product template to display total sale count"""
    _name = 'product.brand'

    name = fields.Char(string='Product Brand')