# -*- coding: utf-8 -*-

from odoo import fields, models


class SaleOrder(models.Model):
    """Extends sales model"""
    _inherit = 'sale.order'

    def action_open_import_lines_wizard(self):
        """ Open the import order lines wizard """
        self.ensure_one()
        print(self)
        return {
            'type': 'ir.actions.act_window',
            'name': 'Import Lines Wizard',
            'res_model': 'import.lines.wizard',
            "views": [[self.env.ref('import_order_lines.view_import_lines_wizard_form').id, "form"]],
            'target': 'new',
            # 'context': {'default_product_uom_id': 'units'}

            # 'context': {'default_product_id': self.id, 'default_price_unit': self.list_price}
        }

