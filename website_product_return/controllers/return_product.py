# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from datetime import datetime
from odoo import _,fields


class ReturnProductController(http.Controller):

    @http.route('/returnformsubmit/<int:id>', type='http', auth='public', website=True)
    def handle_return_form_submission(self, id, **post):
        """Create return for the sale order"""
        sale_order = request.env['sale.order'].sudo().browse(id)
        print(sale_order)

        quantities = request.httprequest.form.getlist('quantity')
        print(quantities)
        print(post)


        receipt = request.env['stock.picking.type'].sudo().search([('code','=','incoming')], limit=1)
        print(receipt)
        picking = sale_order.picking_ids[:1]
        print('picking', picking.name)


        move_commands = []

        for line, quantity in zip(sale_order.order_line,quantities):
            destination = line.move_ids.location_id[:1]
            print(destination)
            move_commands.append(
                fields.Command.create({
                    'product_id': line.product_id.id,
                    'location_id': request.env.user.partner_id.id,
                    'location_dest_id': destination.id,
                    'picking_type_id': receipt.id,
                    'product_uom_qty': quantity,
                    })

            )
            # print('p',line.quantity)

        return_order = request.env['stock.picking'].sudo().create({

            'partner_id': request.env.user.partner_id.id,
            'location_id': request.env.user.partner_id.id,
            'location_dest_id': destination.id,
            'picking_type_id':receipt.id,
            'origin': _("Return of %(picking_name)s", picking_name=picking.name),
            'sale_id': sale_order.id,
            'return_id': picking.id,
            'move_ids': move_commands
        })
        print(return_order.name)

        return request.redirect('/my/orders')

