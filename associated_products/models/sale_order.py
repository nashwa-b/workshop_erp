# -*- coding: utf-8 -*-

from odoo import fields, models, api


class SaleOrder(models.Model):
    """Extends sales model"""
    _inherit = 'sale.order'

    associated_products = fields.Boolean(string='Associated Products')

    # order_id = fields.Many2one(related='res.partner', string='Order')
    # products = fields.Many2many(string='Products', related='res_partner_id.associated_products')
    # res_partner_id = fields.Many2one('res.partner')

    # order_line_ids = fields.One2many(
    #     comodel_name='res.partner',
    #     inverse_name='order_id',
    #     string='Job Order Lines')

    @api.onchange('associated_products')
    def onchange_associated_products(self):
        print(self._origin)
        p = self.order_line.product_id
        u = self.partner_id.associated_product_ids


        if self.associated_products:
            product = self.partner_id.associated_product_ids
            # print(product)
            for i in product:
               # self.order_line.create({
               #          'order_id': self.id,
               #          'product_id': i.id,
               #          # print(partner_id.associated_product_id)
               #          'product_uom_qty': 1,
               #          'price_unit': i.list_price,
               #      })
                self.order_line = [fields.Command.create(
                        {'product_id': i.id,
                        'product_uom_qty': 1,
                        'price_unit': i.list_price})]

                # print(self.product_id)
                print(self.order_line)
        else:
            product = self.partner_id.associated_product_ids
            pro = self.order_line.product_id
            print(product)
            print(pro)
            # print(product)
            for p in product:
                    # order = self.env['sale.order.line'].search([('product_id','=',i.id)])
                    # print(order)
                    # order.unlink()
                    if i.id == j.id:
                        self.order_line.unlink()
                        print(i.id,j.id)
                        print(self.order_line)
                        # print(i.id,j.product_id.id)


                    # # if i.id == j.id:
                    #     self.order_line.unlink(
                    #         {
                    #             {'product_id': i.id,
                    #              'product_uom_qty': 1,
                    #              'price_unit': i.list_price})]
                    #     )
                    #     print(self.order_line)



            #
            # if self.order_line.product_id == self.partner_id.associated_product_ids:
            #     self.order_line.unlink()
            # products = self.order_line.search('self.order_line.product_id','==','self.partner_id.associated_product_ids')
            # products = self.env['res.partner'].search([('associated_product_ids','==',self.order_line.product_id)])
            #
            # # if self.order_line.product_id == self.partner_id.associated_product_ids:
            # products.unlink()
            # orders = self.env['sale.order.line'].search([('order_line', '=', 'cancel')])
            # orders.unlink()
            # product = self.partner_id.associated_product_ids
            # # prod = self.order_line
            # # products = self.partner_id.associated_product_ids
            # domain = [('p', 'in', 'u')]
            # return self.search(domain).unlink()
            # if self.order_line == 'product':
            #     self.order_line.unlink()




