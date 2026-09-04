# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ResPartner(models.Model):
    """Extends partner model"""
    _inherit = 'res.partner'

    vehicle_ids = fields.One2many(
        comodel_name='workshop.vehicle',
        inverse_name='owner_id',
        string='Vehicles',
        copy=True)

    vehicle_count = fields.Integer(
        string='Vehicles',
        compute='_compute_vehicle_count',
        help='Number of vehicles for this partner'
    )

    def action_view_vehicle(self):
        """Open the vehicle view for this partner"""
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "workshop.vehicle",
            "name": "Vehicles",
            "views": [[False, "list"], [False, "form"]],
            "domain": [('owner_id', '=', self.id)],
        }

    @api.depends('name')
    def _compute_vehicle_count(self):
        """Compute the number of vehicle for this partner"""
        for record in self:
            record.vehicle_count = len(record.vehicle_ids)
        # for partner in self:
        #     partner.vehicle_count = self.env['workshop.vehicle'].search_count([('owner_id', '=', partner.id)])
