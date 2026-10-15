# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ProductBrand(models.Model):
    """Product brand model"""
    _name = 'product.brand'

    name = fields.Char(string='Product Brand')