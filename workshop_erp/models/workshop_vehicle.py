# -*- coding: utf-8 -*-

from odoo import models, fields, api


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
    licence_plate = fields.Char(string='License Plate', required=True, tracking=True)
    vin = fields.Char(string='VIN', required=True, tracking=True)
    make = fields.Char(string='Make', tracking=True)
    model = fields.Char(string='Model', tracking=True)
    year = fields.Integer(string='Year', tracking=True)
    odometer = fields.Integer(string='Odometer', required=True, tracking=True)
    owner_id = fields.Many2one('res.partner', string='Owner', required=True, tracking=True)
    active=fields.Boolean(string='Active', default=True, tracking=True)
    job_order_count = fields.Integer(string='Job Orders', compute='_compute_job_order_count')
    job_order_ids = fields.One2many('workshop.job.order','vehicle_id','Job Orders')



    def action_view_job_order(self):
        """Display all previous Job Orders associated with a vehicle"""
        # default_order = self.env['workshop_erp.job_date']._order
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "workshop.job.order",
            "name": "Job Orders",
            "views": [[False, "list"], [False, "form"]],
            "domain": [('vehicle_id', '=', self.id)],
        }

    def _compute_job_order_count(self):
        """Compute the number of Job Order for a vehicle"""
        for record in self:
            record.job_order_count = len(record.job_order_ids)



