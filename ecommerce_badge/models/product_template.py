# -*- coding: utf-8 -*-

from odoo import fields, models


class ProductTemplate(models.Model):
    """Extends product template model to add spare type field."""
    _inherit = 'product.template'

    spare_type = fields.Selection([("genuine","Genuine"), ("oem_oes","OEM / OES"),("aftermarket","Aftermarket")], string='Spare Type')

