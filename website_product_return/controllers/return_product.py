# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from datetime import datetime
from odoo import _,fields


class ReturnProductController(http.Controller):

    @http.route('/returnformsubmit/<int:id>', type='http', auth='public', website=True)
    def handle_return_form_submission(self, id, **post):
        # product = post.get('product'),
        sale_order = request.env['sale.order'].sudo().browse(id)
        print(sale_order)

        quantities = set(request.httprequest.form.getlist('quantity'))
        print(quantities)
        print(post)



        quantity = post.get('quantity')
        # price_unit = post.get('price_unit')
        print(quantity)

        # destination = request.env['stock.location'].sudo().search([], limit=1)
        receipt = request.env['stock.picking.type'].sudo().search([('code','=','incoming')], limit=1)
        # receipt = request.env['stock.location'].sudo().search([('code','=','incoming')], limit=1)
        print(receipt)
        # picking = sale_order.picking_ids.filtered(lambda picking: picking.picking_type_id == 'outgoing')
        picking = sale_order.picking_ids[:1]
        print('picking', picking.name)

        # return_ord = picking.button_validate()
        # return_ord = picking.action_see_returns()
        # print(return_ord)

        # returns = self.env["ir.actions.actions"]._for_xml_id("stock.act_stock_return_picking")
        # print(returns)
        # return returns



        #
        # see = return_ord.action_see_returns()
        # print(see)

        # stock.act_stock_return_picking

        # print(destination)
        # product_ids = set(request.httprequest.form.getlist('product_ids'))
        # line_ids = set(request.httprequest.form.getlist('line_ids'))
        # print('q',line_ids)
        # for line in line_ids:
        #     print('ll',line.quantity)
        # product_ids = [int(lid) for lid in line_ids if lid]

        # print('p',product_ids)

        # line_ids = request.httprequest.form.getlist('line_ids')
        # print('l',line_ids)
        # for line in line_ids:
        #     print(line.product_id)

        # product_ids = [int(pid) for pid in product_ids if pid]
        # products = request.env['product.product'].browse(product_ids)
        # print('pro',products)
        # for product in products:
        #     print(product.location_id)
        #     print(product.location_idq.display_name)

        for line in sale_order.order_line:
            destination = line.move_ids.location_id[:1]
            print(destination)
            # print('p',line.quantity)

        return_order = request.env['stock.picking'].sudo().create({

            'partner_id': request.env.user.partner_id.id,
            'location_id': request.env.user.partner_id.id,
            'location_dest_id': destination.id,
            'picking_type_id':receipt.id,
            'origin': _("Return of %(picking_name)s", picking_name=picking.name),
            'sale_id': sale_order.id,
            'return_id': picking.id,

            'move_ids': [fields.Command.create({
                'product_id': line.product_id.id,
                'location_id': request.env.user.partner_id.id,
                'location_dest_id': destination.id,
                'picking_type_id': receipt.id,
                'product_uom_qty': [for quantity in quantities],
                # 'product_uom': line.uom_id.id,
                # 'location_id': line.source_location_id.id,
                # 'location_dest_id': line.destination_location_id.id,
                # 'picking_type_id': line.picking_type_id.id,
            })for line in sale_order.order_line],
        })
        print(return_order.name)

        return request.redirect('/my/orders')

                # 'phone': post.get('phone'),
                # 'job_date': post.get('job_date'),




        # for product in products:

        # return_order = request.env['stock.picking'].sudo().create({
        #
        #     'partner_id': request.env.user.partner_id.id,
        #     'location_id': request.env.user.partner_id.id,
        #     'location_dest_id': product.location_id.id,
        #     # 'phone': post.get('phone'),
        #     # 'job_date': post.get('job_date'),
        #
        # })






    # @http.route('/return_product', type='http', auth='public', website=True)
    # def return_products(self, **kwargs):
    #     """Display list of job orders of current user"""
    #
    #     print("lkjhg")
    #
    #     product_id = request.env['product.product'].sudo().search([])
    #     # sale_order = self.env['sale.order'].browse(self.env.context.get('active_ids',[]))
    #     sale_order = self.env['sale.order'].browse(self.env.context.get('active_ids',[]))
    #     print('s',sale_order)
    #     current_user = request.env.user.partner_id
    #     print('l', current_user)
    #     current_sale_order = request.env['sale.order.line'].sudo().search([('order_id.partner_id', '=', current_user)])
    #     # print('sale_order', current_sale_order)
    #
    #     # print(product_id)
    #     values = {
    #         'sale_order': current_sale_order,
    #         'products': product_id
    #     }
    #     print(current_sale_order)
    #
    #     # current_user = request.env.user.partner_id
    #     # print('l', current_user)
    #     # job_orders = request.env['workshop.job.order'].sudo().search([('customer_id', '=', current_user)])
    #     # values = {
    #     #     'job_orders': job_orders,
    #     # }
    #     return request.render('website_product_return.product_return_view',values)