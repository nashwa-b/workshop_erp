# -*- coding: utf-8 -*-

from odoo import models, api
from datetime import datetime

class WeatherCondition(models.Model):
    _name = 'weather.condition'

class IrConfig_Parameter(models.Model):
    """IrConfig_Parameter model"""
    _inherit = 'ir.config_parameter'

    @api.model
    def get_weather_parameter(self):
        """ Return weather condition parameter"""
        now = datetime.now()
        formatted_date = now.strftime("%d %B %Y")

        return {
            'latitude':self.sudo().get_param('weather_condition.latitude'),
            'longitude':self.sudo().get_param('weather_condition.longitude'),
            'location':self.sudo().get_param('weather_condition.location'),
            'weather_api_key':self.sudo().get_param('weather_condition.weather_api_keys'),
            'enable_weather':self.sudo().get_param('weather_condition.enable_weather'),
            'status':self.sudo().get_param('weather_condition.state'),
            'formatted_date': formatted_date,
            'date': now
        }