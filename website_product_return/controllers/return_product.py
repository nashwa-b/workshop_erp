# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from datetime import datetime
from odoo import fields


class ReturnProductController(http.Controller):
    @http.route('/return_product', type='http', auth='public', website=True)
    def return_products(self, **kwargs):
        """Display list of job orders of current user"""

        print("lkjhg")

        product_id = request.env['product.product'].sudo().search([])
        # sale_order = self.env['sale.order'].browse(self.env.context.get('active_ids',[]))
        sale_order = self.env['sale.order'].browse(self.env.context.get('active_ids',[]))
        print('s',sale_order)
        current_user = request.env.user.partner_id
        print('l', current_user)
        current_sale_order = request.env['sale.order.line'].sudo().search([('order_id.partner_id', '=', current_user)])
        # print('sale_order', current_sale_order)

        # print(product_id)
        values = {
            'sale_order': current_sale_order,
            'products': product_id
        }
        print(current_sale_order)

        # current_user = request.env.user.partner_id
        # print('l', current_user)
        # job_orders = request.env['workshop.job.order'].sudo().search([('customer_id', '=', current_user)])
        # values = {
        #     'job_orders': job_orders,
        # }
        return request.render('website_product_return.product_return_view',values)