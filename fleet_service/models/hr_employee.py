# -*- coding: utf-8 -*-

from odoo import fields, models, api


class HrEmployee(models.Model):
    """Extends hr employee to add salary levels"""
    _inherit = 'hr.employee'

    is_available_technician =fields.Boolean("Is Available Technician")
    vehicle_ids = fields.Many2many('fleet.vehicle')