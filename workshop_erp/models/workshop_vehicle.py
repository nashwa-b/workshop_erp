# -*- coding: utf-8 -*-

from odoo import models, fields


class WorkshopVehicle(models.Model):
    """ Workshop Vehicle"""
    _name = 'workshop.vehicle'
    _description = 'Vehicle'
    _inherit = ['mail.thread']

    _unique_vin = models.Constraint(
        'UNIQUE(vin)',
        'This vin is already registered!'
    )

    name = fields.Char(required=True, translate=True, tracking=True)
    company_id = fields.Many2one('res.company', string='Company')

    licence_plate = fields.Char(string='License Plate', required=True, tracking=True)
    vin = fields.Char(string='VIN', required=True, tracking=True)
    make = fields.Char(string='Make', tracking=True)
    model = fields.Char(string='Model', tracking=True)
    year = fields.Integer(string='Year', tracking=True)
    odometer = fields.Integer(string='Odometer', required=True, tracking=True)
    owner_id = fields.Many2one('res.partner', string='Owner', required=True, tracking=True)
    active=fields.Boolean(string='Active', default=True, tracking=True)


