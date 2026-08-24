# -*- coding: utf-8 -*-

from odoo import fields, models

from odoo import models, fields


class WorkshopJobLine(models.Model):
    """ Workshop Bay """
    _name = 'workshop.job.line'
    _description = 'Job Lines'

    order_id = fields.Many2one(
        comodel_name='workshop.job.order',
        string='Order Reference',
        ondelete='cascade'
    )

    product_id = fields.Many2one(
        comodel_name='product.product',
        string="Product",
        # change_default=True, ondelete='restrict', index='btree_not_null',
        # domain=lambda self: self._domain_product_id(),
        check_company=True)

    # product_template_id = fields.Many2one(
    #     string="Product Template",
    #     comodel_name='product.template',
    #     compute='_compute_product_template_id',
    #     readonly=False,
    #     search='_search_product_template_id',
    #     domain=lambda self: self._fields['product_id']._description_domain(self.env)
    # )


    product_qty = fields.Float(
        string="Quantity",
        compute='_compute_product_qty',
        digits='Product Unit', default=1.0,
        store=True, readonly=False, required=True, precompute=True)
    # product_uom_id = fields.Many2one(
    #     comodel_name='uom.uom',
    #     string="Unit",
    #     compute='_compute_product_uom_id',
    #     domain='[("id", "in", allowed_uom_ids)]',
    #     store=True, readonly=False, precompute=True, ondelete='restrict')

    price_unit = fields.Float(
        string="Unit Price",
        compute='_compute_price_unit',
        min_display_digits='Product Price',
        store=True, readonly=False, required=True, precompute=True)

    def _compute_price_unit(self):
        self.price_unit=0
    # technical_price_unit = fields.Float()
    #
    #
    #
    # price_subtotal = fields.Monetary(
    #     string="Subtotal",
    #     compute='_compute_amount',
    #     store=True, precompute=True)

    # price_total = fields.Monetary(
    #     string="Total",
    #     compute='_compute_amount'
    #     store=True, precompute=True)


