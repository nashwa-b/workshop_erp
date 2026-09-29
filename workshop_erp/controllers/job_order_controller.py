from odoo import http
from odoo.http import request

class WebsiteCustomerForm(http.Controller):
    @http.route('/website/job_order/form', type='http', auth='public', website=True)
    def customer_form(self, **kw):
        """Render the customer creation form"""
        return request.render('workshop_erp.workshop_list_template')
    @http.route('/website/job_order/create', type='http', auth='public', methods=['POST'], website=True, csrf=True)
    def create_customer(self, **post):
        """Handle form submission and create a new customer"""
        name = post.get('name')
        email = post.get('email')
        phone = post.get('phone')
        if not name:
            # If name is missing, redirect back to form with an error message
            return request.render('workshop_erp.workshop_list_template', {
                'error': 'Name is required!'
            })
        request.env['res.partner'].sudo().create({
            'name': name,
            'email': email or False,
            'phone': phone or False,
            'customer_rank': 1,
        })
        return request.render()
