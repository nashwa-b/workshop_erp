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

    @http.route('/newjoborder', type='http',  auth='public', website=True ,csrf=False)
    def display_web_form(self, **kw):
        # price_unit = self.product_id.list_price
        customers = request.env['res.partner'].sudo().search([])
        vehicles = request.env['workshop.vehicle'].sudo().search([])
        mechanics = request.env['hr.employee'].sudo().search([])
        job_types = request.env['job.type'].sudo().search([])
        bay_id = request.env['workshop.bay'].sudo().search([])
        product_id = request.env['product.product'].sudo().search([])
        user_name = request.env.user.name if request.env.user.id else 'Guest'
        phone = request.env.user.phone
        dates = datetime.today()
        # product= kw.get('product_id')
        # product = kw.get('product_id').read()
        # product = kw.get('name').sudo().read()
        # print('p',product)
        # mechanic_ids = [int(x) for x in request.httprequest.form.getlist('mechanics')]

        values = {
            'customers': customers,

            'vehicles': vehicles,
            # 'mechanic_ids': mechanics,
            'job_types': job_types,
            'bays': bay_id,
            'products': product_id,
            'user_name': user_name,
            'phone': phone,
            'dates': dates,
            # 'price_unit': product

        }
        return request.render('workshop_erp.web_form_template',values)

    @http.route('/webformsubmit', type='http', auth='public', website=True, csrf=False)
    # @http.route('/webformsubmit', type='http', auth='user', methods=['POST'], website=True )
    def handle_web_form_submission(self, **post):
        print('lkk',self)
        mechanic_ids = [int(x) for x in request.httprequest.form.getlist('mechanic_ids')]

        job_order = request.env['workshop.job.order'].sudo().create({
            'customer_id':post.get('customer_id'),
            'phone':post.get('phone'),
            'job_date':post.get('job_date'),
            # 'customer_id': post.get('customer_id'),
            # 'phone': post.get('phone'),
            'vehicle_id': post.get('vehicle_id'),
            # 'mechanic_ids': post.get('mechanic_ids'),
            'job_type_id': post.get('job_type_id'),
            'bay_id': post.get('bay_id'),
            'total': post.get('total'),

            'mechanic_ids': [(6, 0, mechanic_ids)],

        })
        return request.render('workshop_erp.submit_template',{
            'job_order': job_order
        })

        # mechanic_ids = [int(x) for x in request.httprequest.form.getlist('mechanic_ids')]

        # mechanic_ids = post.getlist('mechanic_ids')
        # mechanic_ids = list(map(int, mechanic_ids)) if mechanic_ids else []
        # request.env['workshop.job.order'].sudo().create({
        #     'customer_id':post.get('name'),
        #     'phone':post.get('phone'),
        #     'job_date':post.get('job_date'),
        #     # 'customer_id': post.get('customer_id'),
        #     # 'phone': post.get('phone'),
        #     'vehicle_id': post.get('vehicle_id'),
        #     # 'mechanic_ids': post.get('mechanic_ids'),
        #     'job_type_id': post.get('job_type_id'),
        #     'bay_id': post.get('bay_id'),
        #     'total': post.get('total'),
        #     'product_id': post.get('product_id'),
        #     # 'mechanic_ids': [(6, 0, mechanic_ids)],
        #
        # })
        # return request.render('workshop_erp.submit_template')

    @http.route('/appointments', type='http', auth='public', website=True, csrf=False)
    def display_appointment(self, **post):
        # price_unit = self.product_id.list_price
        job_orders = request.env['workshop.job.order'].sudo().search([])
        vehicles = request.env['workshop.vehicle'].sudo().search([])
        customer = request.env['res.partner'].sudo().search([])

        # orders = request.env['workshop.job.order'].sudo().create({
        #     'customer_id': post.get('name'),
        #     'job_date': post.get('date'),
        #     'vehicle_id': post.get('vehicle_id'),
        # })
        values={
            'customer': customer,
            'job_orders': job_orders,
            'vehicles': vehicles,
            # 'orders':orders
        }
        return request.render('workshop_erp.appointment', values)

    @http.route('/createappointment', type='http', auth='public', methods=['POST'], website=True, csrf=True)
    def create_appointment(self, **post):
        print('p',self)
        """Handle form submission and create a new customer"""
        customer = post.get('customer_id')
        date = post.get('date')

        vehicle = post.get('vehicle_id')

        job_order = request.env['workshop.job.order'].sudo().create({
            'customer_id': customer,
            'job_date': date,
            'vehicle_id': vehicle,
        })


        request.env['calendar.event'].sudo().create({
            'name':post.get('name'),
            # 'start':post.get('start_date'),
            # 'stop':post.get('end_date'),
            # 'job_order_id': job_order.name
        })

