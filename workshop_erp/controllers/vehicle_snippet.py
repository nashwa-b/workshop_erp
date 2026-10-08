# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
class WebsiteVehicle(http.Controller):
   @http.route('/get_top_vehicles', auth="public", type='jsonrpc',website=True)
   def get_top_vehicles(self):
       """Get the Top Vehicles."""
       # vehicles = request.env['workshop.vehicle'].search([])
       vehicles = request.env['workshop.vehicle'].search_read(
          fields=['name', 'id','image','licence_plate','vin','model'], order = 'job_order_count DESC', limit = 10
       )

       print(vehicles)
       values = {
           'vehicles': vehicles,
       }
       return values

   @http.route('/vehicleview/<int:id>', type='http', auth='public', website=True)
   def view_vehicle(self, id):
       """Get the vehicle using id and display its details."""
       vehicle = request.env['workshop.vehicle'].sudo().browse(id)

       return request.render('workshop_erp.vehicle_view', {
           'vehicle': vehicle
       })
