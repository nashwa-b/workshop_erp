# -*- coding: utf-8 -*-

from odoo import fields, models, api


class PurchaseOrder(models.Model):
    """Extends purchase to add limit to the total purchase amount"""
    _inherit = 'purchase.order'

    material_request_id = fields.Many2one('material.request', 'Material Request')
