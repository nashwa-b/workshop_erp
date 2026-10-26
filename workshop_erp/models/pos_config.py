from odoo import models, fields


class PosConfig(models.Model):
    _inherit = 'pos.config'

    category_wise_discount = fields.Boolean(string="Enable Category-Wise Discount")
    m_max_discount_ids= fields.One2many('pos.category','con_id', readonly=False)

