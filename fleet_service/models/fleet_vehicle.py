# -*- coding: utf-8 -*-

from odoo import fields, models, api


class FleetVehicle(models.Model):
    """Extends hr employee to add salary levels"""
    _inherit = 'fleet.vehicle'

    service_blocked = fields.Boolean('Service Blocked')