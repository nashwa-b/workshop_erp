# -*- coding: utf-8 -*-

from odoo import fields, models,api


class ResConfigSettings(models.TransientModel):
    """Extend product variants view to display average cost of that product from all purchase orders"""
    _inherit = 'res.config.settings'

    # location = fields.Char(string="Location", config_parameter='weather_notification.location',groups = "base.group_system")
    latitude = fields.Float(string="Latitude")
    longitude = fields.Float(string="Longitude")
    weather_api_keys = fields.Char(string="API Key", config_parameter='weather_notification.weather_api_key',groups = "base.group_system")
    enable_weather = fields.Boolean(string="Enable Weather",config_parameter='weather_notification.enable_weather', default=True,groups = "base.group_system")

    # groups = "base.group_system"

    def fetch_location(self,coords):
            # current_user = self.env.user
            # related_partner = current_user.partner_id

        self.latitude = coords.get('latitude')
        self.longitude = coords.get('longitude')

        return

    def manual_location(self):
        pass


