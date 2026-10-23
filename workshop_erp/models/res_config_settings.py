# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    """Extends partner model by adding smart buttons for vehicles and job orders associated with that partner"""
    _inherit = 'res.config.settings'

    category_wise_discount = fields.Boolean(string="Enable Category-Wise Discount", default=True)

    @api.model
    def _load_pos_data_fields(self, config_id):
        data = super()._load_pos_data_fields(config_id)
        data += ['category_wise_discount']
        return data

