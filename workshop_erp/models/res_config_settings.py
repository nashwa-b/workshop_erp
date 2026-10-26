# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    """Extends partner model by adding smart buttons for vehicles and job orders associated with that partner"""
    _inherit = 'res.config.settings'

    enable_category_wise_discount = fields.Boolean(related='pos_config_id.category_wise_discount', readonly=False, default=True)
    # max_discount = fields.One2many(related='pos_config_id.max_discount', readonly=False)
    max_discount_ids= fields.One2many(related='pos_config_id.m_max_discount_ids', readonly=False)

    # ldaps = fields.One2many(related='company_id.ldaps', string="LDAP Parameters", readonly=False)



    # pos_discount_pc = fields.Float(related='pos_config_id.discount_pc', readonly=False)



    @api.model
    def _load_pos_data_fields(self, config_id):
        params = super()._load_pos_data_fields(config_id)
        # param_value = self.env['ir.config_parameter'].sudo().get_param('point_of_sale.category_wise_discount')
        # print(param_value)
        params += ["enable_category_wise_discount"]
        print(params)
        return params




