# -*- coding: utf-8 -*-

from odoo import fields, models

class WeatherCondition(models.Model):
    """workshop job types"""
    _name = 'weather.condition'
    _description = 'Weather Condition'

    weather_id = fields.Many2one('res.config.settings', 'Weather Condition', required=True)
    location = fields.Char(string="Location")
    weather_api_key = fields.Char(string="API Key")


