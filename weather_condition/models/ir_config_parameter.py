# -*- coding: utf-8 -*-

from odoo import fields, models, api
from datetime import datetime

class WeatherCondition(models.Model):
    _name = 'weather.condition'

class IrConfig_Parameter(models.Model):
    """workshop job types"""
    _inherit = 'ir.config_parameter'

    @api.model
    def get_weather_parameter(self):
        now = datetime.now()
        formatted_date = now.strftime("%d %B %Y")

        return {
            'location':self.sudo().get_param('weather_notification.location'),
            'weather_api_key':self.sudo().get_param('weather_notification.weather_api_key'),
            'formatted_date': formatted_date,
            'date': now
        }