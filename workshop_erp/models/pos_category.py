# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.exceptions import ValidationError


class PosCategory(models.Model):
    """Extends pos.category model to add new field to restrict max discount allowed to that category"""
    _inherit = 'pos.category'

    max_discount = fields.Float(string="Discount(%)", default=0)

    @api.constrains('max_discount')
    def _check_discount(self):
        for category in self:
            if not 0<=category.max_discount<=100:
                raise ValidationError("Discount must be between 0 and 100")


    @api.model
    def _load_pos_data_fields(self, config):
        fields = super()._load_pos_data_fields(config)
        fields += ['max_discount']
        print(fields)
        return fields

