# -*- coding: utf-8 -*-

from odoo import models,fields, api


class ProductTemplate(models.Model):
    """Extends product template to load spare_type field into pos"""
    _inherit = 'product.template'

    spare_type_label = fields.Char(
        string='Spare Type Label',
        compute='_compute_spare_type_label',
    )

    @api.depends('spare_type')
    def _compute_spare_type_label(self):
        """Compute spare type label"""
        selection = dict(self._fields['spare_type'].selection)
        for product in self:
            product.spare_type_label = selection.get(
                product.spare_type, ''
            )

    @api.model
    def _load_pos_data_fields(self, config_id):
        """Load spare type label field into pos"""
        data = super()._load_pos_data_fields(config_id)
        for field in ('spare_type', 'spare_type_label'):
            if field not in data:
                data.append(field)
        print(data)
        return data

