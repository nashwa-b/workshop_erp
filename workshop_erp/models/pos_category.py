# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.exceptions import ValidationError


class PosCategory(models.Model):
    """Extends partner model by adding smart buttons for vehicles and job orders associated with that partner"""
    _inherit = 'pos.category'

    max_discount = fields.Float(string="Discount(%)", default=0)
    con_id = fields.Many2one('pos.config','id')
    names = fields.Many2one('pos.category','name')

    @api.constrains('max_discount')
    def _check_discount(self):
        for category in self:
            if not 0<=category.max_discount<=100:
                raise ValidationError("Discount must be between 0 and 100")


    @api.model
    def _load_pos_data_fields(self, config):
        fields = super()._load_pos_data_fields(config)
        # if self.max_discount not in fields:
        fields += ['max_discount']

        print(fields)
        return fields

    # @api.model
    # def _load_pos_data_fields(self, config):
    #     fields = super()._load_pos_data_fields(config)
    #     fields += ['event_ticket_id', 'event_registration_ids']
    #     return fields


