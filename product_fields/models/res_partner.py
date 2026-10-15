# -*- coding: utf-8 -*-

from odoo import fields, models


class ResPartner(models.Model):
    """Extends res partner to add prime customer"""
    _inherit = 'res.partner'

    is_prime_customer = fields.Boolean(string="Is Prime Customer", default=False)