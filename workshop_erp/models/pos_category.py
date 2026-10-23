# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.exceptions import ValidationError


class PosCategory(models.Model):
    """Extends partner model by adding smart buttons for vehicles and job orders associated with that partner"""
    _inherit = 'pos.category'

    discount = fields.Float(string="Discount(%)", default=0)

    @api.constrains('discount')
    def _check_discount(self):
        for category in self:
            if not 0<=category.discount<=100:
                raise ValidationError("Discount must be between 0 and 100")

    @api.model
    def _load_pos_data_fields(self, config_id):
        data = super()._load_pos_data_fields(config_id)
        data += ['discount']
        return data