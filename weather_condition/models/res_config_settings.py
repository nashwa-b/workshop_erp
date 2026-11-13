# -*- coding: utf-8 -*-

from odoo import fields, models,api


class ResConfigSettings(models.TransientModel):
    """ResConfigSettings model"""
    _inherit = 'res.config.settings'

    location = fields.Char(string="Location", config_parameter='weather_notification.location',groups = "base.group_system")
    latitude = fields.Float(string="Latitude", config_parameter='weather_notification.latitude')
    longitude = fields.Float(string="Longitude", config_parameter='weather_notification.longitude')
    weather_api_keys = fields.Char(string="API Key", config_parameter='weather_notification.weather_api_key',groups = "base.group_system")
    enable_weather = fields.Boolean(string="Enable Weather",config_parameter='weather_notification.enable_weather', default=False,groups = "base.group_system")
    state = fields.Selection(
        [('fetch_location', 'Fetch Location'), ('manual_location', 'Manual Location')],
        string='Mode', default=False,)

    def manual_location(self):
        return {
            'latitude': self.latitude,
            'longitude': self.longitude,
        }
