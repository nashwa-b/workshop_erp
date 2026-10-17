# -*- coding: utf-8 -*-

from odoo import fields, models
from datetime import datetime, timedelta, time


class SaleOrder(models.Model):
    """Extends sales model"""
    _inherit = 'sale.order'

    def action_confirm(self):
        """Create purchase order for each order line in sale order"""
        print('p', self)
        res = super(SaleOrder, self).action_confirm()
        for order in self:
            for line in order.order_line:
                product = line.product_id
                print("l", product)
                vendor_id = product.seller_ids[:1]
                vendor = vendor_id.partner_id
                print("Srf", order, order.id)
                po = self.env['purchase.order'].create({
                    'partner_id': vendor.id,
                    'order_line': [fields.Command.create({
                        'product_id': product.id,
                        'product_qty': line.product_qty,
                        'price_unit': line.price_unit,
                        'price_subtotal': line.price_subtotal,
                        'sale_line_id': line.id,
                    })],
                })

                print("fedsgh", po, order.id, self.id)
                print("fedsgh11", po, po.order_line)
                print("fedsgh11", po, po.order_line.sale_line_id)
        return res

    def _create_so_po_history(self):
        """Create SO PO history of previous day"""
        print("so", self)
        # yesterday = datetime.today()
        yesterday = datetime.now() - timedelta(days=1)
        print(yesterday)
        print(yesterday.strftime('%y-%m-%d'))
        day_start = datetime.combine(yesterday, time.min)
        day_end = datetime.combine(yesterday, time.max)
        record = self.search([('date_order', '>=', day_start), ('date_order', '<=', day_end)])
        print('record', record)
        print(day_start, day_end)
        for rec in record:
            print('rec', rec.id)
            for line in rec.order_line:
                print('line', line.id)
                vendor = line.product_id.mapped('seller_ids.partner_id')
                po_lines = self.env['purchase.order.line'].search([
                    ('product_id', '=', line.product_id.id),
                    ('sale_line_id', '=', line.id)
                ])
                purchases = po_lines.mapped('order_id')
                print("jghhf", po_lines)
                print("fedsgh11", po_lines, po_lines.sale_line_id)

                history = self.env['sale.purchase.history'].search([('sale_id','=',rec.id)])
                if history:
                    history.write({
                        'purchase_ids': [fields.Command.link(id) for id in purchases.ids],
                    })
                    print('lll')

                else:
                     self.env['sale.purchase.history'].create({
                        'sale_id': rec.id,
                        'date': self.date_order,
                        'vendor_ids': [fields.Command.set(vendor.ids)],
                        'partner_id': rec.partner_id.id,
                        'purchase_ids': [fields.Command.set(purchases.ids)],
                        'salesperson_id': rec.user_id.id
                    })
            #         print('kkk')
            #
            #
            # print("fedsgh11", po)
            # print("fedsgh11", po.purchase_ids)
            # print("fedsgh11", po.vendor_ids)
            #

