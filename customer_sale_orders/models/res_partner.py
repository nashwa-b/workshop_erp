# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ResPartner(models.Model):
    """Extends product template model to add spare type field."""
    _inherit = 'res.partner'


    sale_order_ids = fields.One2many('sale.order', 'partner_id', string='Sales Orders')
    # purchase_line_ids = fields.One2many('purchase.order.line', 'partner_id', string='Purchase Orders')
    product_count = fields.Integer(compute='_compute_products', string='Product Count')
    products = fields.Integer(compute='_compute_products', string='Products')

    @api.depends('purchase_line_ids')
    def _compute_products(self):
        """Total Amount"""
        for record in self:
            record.product_count = len(self.sale_order_ids)

            # record.products = record.purchase_line_ids.mapped('product_id').ids
            # print(record.products)


    def action_view_products(self):
        """Open the vehicle view for this partner in smart button"""
        self.ensure_one()

        return {
            "type": "ir.actions.act_window",
            "res_model": "product.product",
            "name": "Products",
            # "view_id":  self.env.ref("product.product_product_tree_view").id,
             "views": [[self.env.ref("product.product_product_tree_view").id, "list"]],
            "domain":[('id', 'in', self.sale_order_ids.order_line.mapped('product_id').ids),(self.sale_order_ids.mapped('state'),'=',self.env.ref('send'))]
            # "domain":[('id' in self.products)]
             # "views": [[self.purchase_line_ids, "list"]],
            # "domain": [(self.id ,'=',  self.products)],
        }




