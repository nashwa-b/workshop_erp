# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
class WebsiteVehicle(http.Controller):
   @http.route('/get_top_vehicles', auth="public", type='jsonrpc',
               website=True)
   def get_top_vehicles(self):
       """Get the website categories for the snippet."""
       # vehicles = request.env['workshop.vehicle'].search([])
       vehicles = request.env['workshop.vehicle'].search_read(
          fields=['name', 'id'], order = 'job_order_count DESC', limit = 4
       )
       print(vehicles)

       # search([('limit', '<', record.amount_total)], order='limit desc', limit=1)
       # public_categs = request.env[
       #     'product.public.category'].sudo().search_read(
       #     [('parent_id', '=', False)], fields=['name', 'image_1920', 'id']
       # )
       values = {
           'vehicles': vehicles,
       }
       return values

   @http.route('/vehicleview/<int:id>', type='jsonrpc', auth='public', website=True)
   def view_vehicle(self, id):
       """Display form of job orders in list view"""
       vehicle = request.env['workshop.vehicle'].sudo().browse(id)
       return request.render('workshop_erp.job_order_view', {
           'vehicle': vehicle
       })

   # @http.route('/joborderview/<int:id>', type='http', auth='public', website=True)
   # def view_job_orders(self, id):
   #     """Display form of job orders in list view"""
   #     job_order = request.env['workshop.job.order'].sudo().browse(id)
   #     return request.render('workshop_erp.job_order_view', {
   #         'job_order': job_order
   #     })

