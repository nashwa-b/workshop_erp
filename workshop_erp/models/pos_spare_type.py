# -*- coding: utf-8 -*-


from odoo import models, api

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model
    def _load_pos_data_fields(self, config_id):
        data = super()._load_pos_data_fields(config_id)
        data.append('spare_type')
        return data