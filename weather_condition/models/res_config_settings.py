# -*- coding: utf-8 -*-

from odoo import fields, models,api


class ResConfigSettings(models.TransientModel):
    """Extend product variants view to display average cost of that product from all purchase orders"""
    _inherit = 'res.config.settings'

    location = fields.Char(string="Location", config_parameter='weather_notification.location')
    weather_api_keys = fields.Char(string="API Key", config_parameter='weather_notification.weather_api_key')


