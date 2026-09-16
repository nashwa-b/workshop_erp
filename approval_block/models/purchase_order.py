# -*- coding: utf-8 -*-

from odoo import fields, models, api


class PurchaseOrder(models.Model):
    """Extends sales model"""
    _inherit = 'purchase.order'


    limit_id = fields.Many2one(string="Limit", comodel_name='approval.block',compute="_compute_limit",store=True,inverse="_inverse_total")

    @api.depends('amount_total')
    def _compute_limit(self):
        """Compute total limit amount on purchase order"""
        for record in self:
            record.limit_id = self.env['approval.block'].search([('limit', '<', record.amount_total)], order='limit desc', limit=1)

    def _inverse_total(self):
        """make the limit field editable"""
        for record in self:
            pass
