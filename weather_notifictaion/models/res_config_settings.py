# -*- coding: utf-8 -*-

from odoo import fields, models,api


class ResConfigSettings(models.TransientModel):
    """Extend product variants view to display average cost of that product from all purchase orders"""
    _inherit = 'res.config.settings'

    location = fields.Char(string="Location", related="weather_id.location")
    weather_api_key = fields.Char(string="API Key", related="weather_id.weather_api_key")

