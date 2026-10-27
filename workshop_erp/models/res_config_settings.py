# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    """Extends conf settings to add new boolean to validate max discount"""
    _inherit = 'res.config.settings'

    enable_category_wise_discount = fields.Boolean(related='pos_config_id.category_wise_discount', readonly=False, default=True)

    @api.model
    def _load_pos_data_fields(self, config_id):
        """Load boolean to pos data fields"""
        params = super()._load_pos_data_fields(config_id)
        params += ["enable_category_wise_discount"]
        print(params)
        return params




