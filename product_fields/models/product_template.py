# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ProductTemplate(models.Model):
    """Extends product template to display brand and master type"""
    _inherit = 'product.template'

    product_brand_id = fields.Many2one(string='Product Brand', comodel_name='product.brand')
    product_master_type = fields.Selection([('single_product','Single Product'),("branded_product","Branded Product")],string="Product Master Type", default='single_product')
