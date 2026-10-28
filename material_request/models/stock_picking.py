# -*- coding: utf-8 -*-

from odoo import fields, models, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    material_request_id = fields.Many2one('material.request', 'Material Request')
