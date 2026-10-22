# -*- coding: utf-8 -*-


from odoo import models, api

class ProductProduct(models.Model):
    _inherit = 'product.template'

    @api.model
    def _load_pos_data_fields(self, config_id):
        # Call super() to keep existing fields and append your target field
        field_list = super()._load_pos_data_fields(config_id)
        field_list.append('spare_type')
        return field_list