# -*- coding: utf-8 -*-

from odoo import fields, models
from datetime import datetime, timedelta, time


class SaleOrder(models.Model):
    """Extends sales model"""
    _inherit = 'sale.order'

    def action_confirm(self):
        print('p',self)
        res = super(SaleOrder, self).action_confirm()
        for order in self:
            for line in order.order_line:
                product = line.product_id
                print("l",product)
                vendor_id = product.seller_ids[:1]
                vendor = vendor_id.partner_id
            # for self.order_line in self:
                po = self.env['purchase.order'].create({
                    'partner_id': vendor.id,
                    # 'partner_id': self.partner_id.id,
                    'order_line': [fields.Command.create({
                            'product_id': product.id,
                            'product_qty': line.product_qty,
                            'price_unit': line.price_unit,
                            # 'product_uom_id': line.product_uom_id,
                            'price_subtotal': line.price_subtotal,
                    })],
                    })
                print('po',po)
        return res

    def _create_so_po_history(self):
        print("so",self)
        tomorrow = datetime.now() + timedelta(days=1)
        print(tomorrow)
        # print(tomorrow.strftime('%y-%m-%d'))
        # tom = tomorrow.strftime('20%y-%m-%d')
        day_start = datetime.combine(tomorrow, time.min)
        day_end = datetime.combine(tomorrow, time.max)
        record = self.search([('date_order', '>=', day_start), ('date_order', '<=', day_end)])
        print(day_start, day_end)
        for rec in record:
            for line in rec.order_line:
                vendor = line.product_id.seller_ids
                self.env['sale.purchase.history'].create({
                    'sale_id': self.id,
                    'date': self.date_order,
                    'vendor_ids': vendor.ids,
                    'partner_id': self.partner_id.id,
                    'purchase_ids': line.product_id.purchase_order_line_ids.order_id.id,
                    'salesperson_id': self.user_id.id

                })

        # sale_id, purchase_ids, partner_id, date, salesperson_id and vendor_ids

        # record = self.envsearch([('start', '>=', day_start), ('start', '<=', day_end)])
        # for rec in record:
        #     mail_template = self.env.ref('workshop_erp.mail_template_calendar_event')
        #     email_values = {'email_to': rec.customer_id.email}
        #     mail_template.send_mail(rec.id, force_send=True, email_values=email_values)

        # """
        # Automated method to send a follow-up email to partners.
        # """
        # # Example: Fetch all partners who are customers
        # customer_records = self.search([('customer_rank', '>', 0)])
        #
        # # Get an email template from the system
        # mail_template = self.env.ref('my_module.email_template_daily_followup')
        #
        # # Send the template to each customer
        # for partner in customer_records:
        #     mail_template.send_mail(partner.id, force_send=False)  # force_send=False queues the email

        # res = super(SaleOrder, self).action_confirm()
        # self.job_order_id.status = 'confirmed'
        # print(self.job_order_id)

        # })

