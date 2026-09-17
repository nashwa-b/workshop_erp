# -*- coding: utf-8 -*-

from odoo import fields, models


class SaleOrderWizard(models.TransientModel):
    """Creation of Wizards for Sales Orders"""
    _name = 'sale.order.wizard'
    _description = 'Wizard for Sales Orders'

    customer_id = fields.Many2one('res.partner', string="Customer")
    quantity = fields.Float(string="Quantity", default=1)
    price_unit = fields.Float(string="Unit Price")
    product_id = fields.Many2one('product.product', string="Product")


    def action_create_sale_order(self):
        """Sale Order Creation"""
        self.ensure_one()
        sale_order = self.env['sale.order'].search([('state', '=', 'draft'),('partner_id','=', self.customer_id)],limit=1)
        print('j',sale_order)
        if not sale_order:

            sale_order = self.env['sale.order'].create({
                'partner_id': self.customer_id.id,
                'order_line': [
                    fields.Command.create({
                        'product_id': self.product_id.id,
                        'product_uom_qty': 1,
                        'price_unit': self.price_unit,
                    }),
                ],
            })

        else:
            sale_order.write({
                'order_line': [
                    fields.Command.create({
                        'product_id': self.product_id.id,
                        'product_uom_qty': 1,
                        'price_unit': self.price_unit,
                    }),
                ],
            })
        sale_order.action_confirm()
        return self.action_view_sale_order(sale_order)

    def action_view_sale_order(self, sale_order):
        """View Sale Order Creation"""
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Quotation',
            'res_id': sale_order.id,
            'res_model': 'sale.order',
            "views": [[False, "form"]],
            'target': 'current'
        }




