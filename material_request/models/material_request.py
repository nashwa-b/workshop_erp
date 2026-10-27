# -*- coding: utf-8 -*-

from odoo import fields, models, api


class MaterialRequest(models.Model):
    """Employee Loan"""
    _name = 'material.request'
    _description = 'Material Request'
    _inherit = ['mail.thread']

    name = fields.Char('Name', readonly=True, default='New')

    @api.model_create_multi
    def create(self, vals_list):
        """Sequence Creation"""
        print(self)
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('material.request') or 'New'
        return super().create(vals)
