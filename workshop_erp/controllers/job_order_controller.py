# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from datetime import datetime

class JobOrderController(http.Controller):
    @http.route('/joborders', type='http', auth='public', website=True)
    def display_job_orders(self, **kwargs):
        print('l',self)
        job_orders = request.env['workshop.job.order'].sudo().search([])
        print('k', job_orders)
        # values = {
        #     'job_orders': job_orders,
        #     'page_name': job_orders
        # }
        return request.render('workshop_erp.portal_job_orders', {
            'job_orders': job_orders
        })

    @http.route('/newjoborder', type='http',  auth='public', website=True)
    def display_web_form(self, **kwargs):
        # price_unit = self.product_id.list_price
        vehicles = request.env['workshop.vehicle'].sudo().search([])
        mechanics = request.env['hr.employee'].sudo().search([])
        job_types = request.env['job.type'].sudo().search([])
        bay_id = request.env['workshop.bay'].sudo().search([])
        product_id = request.env['product.product'].sudo().search([])
        user_name = request.env.user.name if request.env.user.id else 'Guest'
        phone = request.env.user.phone
        dates = datetime.today()

        values = {
            'vehicles': vehicles,
            'mechanics': mechanics,
            'job_types': job_types,
            'bays': bay_id,
            'products': product_id,
            'user_name': user_name,
            'phone': phone,
            'date': dates,
            # 'price_unit': price_unit,


        }
        return request.render('workshop_erp.web_form_template',values)

    @http.route('/webformsubmit', type='http', auth='public', website=True, methods=['POST'])
    def handle_web_form_submission(self, **post):
        print('lkk',self)
        request.env['workshop.job.order'].sudo().create({
            # 'customer_id': post.get('customer_id'),
            # 'phone': post.get('phone'),
            'vehicle_id': post.get('vehicle_id'),
            'mechanic_ids': post.get('mechanic_ids'),
            'job_type_id': post.get('job_type_id'),
            'bay_id': post.get('bay_id'),
            'job_date': post.get('job_date'),
            'total': post.get('total'),
            'products': post.get('products'),

        })
        return request.redirect('workshop_erp.submit_template')


