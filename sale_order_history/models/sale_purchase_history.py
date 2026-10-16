# -*- coding: utf-8 -*-

from odoo import fields, models, api


class SalePurchaseHistory(models.Model):
    """Sale and its purchase order history"""
    _name = 'sale.purchase.history'

    sale_id = fields.Many2one('sale.order', string='Sale Order')
    purchase_ids = fields.Many2many('purchase.order', string='Purchases')
    partner_id = fields.Many2one('res.partner', string='Customer')
    date = fields.Datetime(string='Date of purchase')
    salesperson_id = fields.Many2one('res.users', string='Salesperson')
    vendor_ids = fields.Many2many('res.partner', string='Vendors')

