# -*- coding: utf-8 -*-

from odoo import fields, models

from io import BytesIO
import base64
import openpyxl

class ImportLinesWizard(models.TransientModel):
    """Creation of Wizards for Import Order Lines"""
    _name = 'import.lines.wizard'
    _description = 'Wizard for Import Lines'

    import_file = fields.Binary(string="Import File")
    filename = fields.Char(string="File Name")

    def import_xls(self):
        """  Import xlsx report to SaleOrder line """
        wb = openpyxl.load_workbook(
            filename=BytesIO(base64.b64decode(self.import_file)),
            read_only=True
        )
        ws = wb.active


        for record in ws.iter_rows(min_row=2, max_row=None, min_col=None,
                                   max_col=None, values_only=True):
            active_id = self.env.context.get('active_id')
            product = self.env['product.product'].search([('name', '=', record[0])],limit=1)
            unit = self.env['uom.uom'].search([('name', '=', record[2])],limit=1)
            default_uom = self.env['uom.uom'].search([('name', '=', 'Units')],limit=1)
            unit_record = record[2]

            if not product:
                product = self.env['product.product'].create({
                    'name': record[0]})

            if not unit_record:
                # pass
                unit = default_uom

            if not unit:
                unit = self.env['uom.uom'].create({
                    'name': unit_record})


            new = self.env['sale.order.line'].create({
                'order_id': active_id,
                'display_type': False,
                'product_id': product.id,
                'name': record[3],
                'price_unit': record[4],
                'product_uom_qty': record[1],
                'product_uom_id': unit.id,
            })

        return new
