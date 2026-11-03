# -*- coding: utf-8 -*-

from odoo import _, fields, models, service, api
from odoo.tools import urls

from odoo.addons.payment.logging import get_payment_logger
from odoo.addons.payment_mollie import const
from odoo.tools.urls import urljoin



import requests
from odoo.exceptions import ValidationError
from odoo.tools import urls
# from odoo.addons.payment_multisafepay.controllers.main import MultisafepayController
from odoo.addons.payment.const import CURRENCY_MINOR_UNITS




import logging
from decimal import Decimal
#
# from payment_multisafepay.sdk import Sdk
# from multisafepay.transport import RequestsTransport

# from odoo.addons.payment import const

#
from odoo.addons.payment.logging import get_payment_logger
# from odoo.addons.payment_multisafepay import const
# from .. import const


_logger = get_payment_logger(__name__)


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('multisafepay', 'MultiSafepay')], ondelete={'multisafepay': 'set default'}
    )

    multisafepay_api_key = fields.Char(
        string="MultiSafepay API Key",
        help="The Test or Live API Key depending on the configuration of the provider",
        required_if_provider='multisafepay',
        copy=False,
        groups='base.group_system',
    )

    # def get_multisafepay_url(self,api_state):
    #     if api_state == 'enabled':
    #         'https://api.multisafepay.com/v1/json/orders'
    #     return 'https://testapi.multisafepay.com/v1/json/orders'


    def _get_redirect_form_view(self, is_validation=False):
        _logger.info("Form view")

        """ Override of `payment` to avoid rendering the form view for validation operations.

        Unlike other compatible payment methods in Xendit, `Card` is implemented using a direct
        flow. To avoid rendering a useless template, and also to avoid computing wrong values, this
        method returns `None` for Xendit's validation operations (Card is and will always be the
        sole tokenizable payment method for Xendit).

        Note: `self.ensure_one()`

        :param bool is_validation: Whether the operation is a validation.
        :return: The view of the redirect form template or None.
        :rtype: ir.ui.view | None
        """
        self.ensure_one()

        if self.code == 'multisafepay' and is_validation:
            return self.env.ref('payment_multisafepay.multisafepay_form')
        return super()._get_redirect_form_view(is_validation=is_validation)

    # def _build_request_url(self, endpoint, **kwargs):
    #     _logger.info("Generated MultiSafepay URL")
    #     """ Build the MultiSafepay request URL dynamically based on environment state. """
    #     self.ensure_one()
    #     if self.state == 'enabled':
    #         base_url = 'https://api.multisafepay.com/v1/json/'
    #     else:
    #         base_url = 'https://testapi.multisafepay.com/v1/json/'
    #
    #     # return urljoin(base_url, endpoint)
    #
    #
    #     endpoint = endpoint.lstrip('/')
    #     return f"{base_url}{endpoint}"

    def _build_request_url(self, endpoint, **kwargs):
        """Override of `payment` to build the request URL."""
        if self.code != 'multisafepay':
            return super()._build_request_url(endpoint, **kwargs)

        if self.state == 'enabled':
            api_url = 'https://api.multisafepay.com/v1/json'
        else:
            api_url = 'https://testapi.multisafepay.com/v1/json'

        return urljoin(api_url, endpoint)


    def _build_request_headers(self, method, endpoint, payload, **kwargs):
        """ Build the headers for the MultiSafepay request. """
        return {
            "accept": "application/json",
            "content-type": "application/json",
            'Authorization': f'Bearer {self.multisafepay_api_key}',
        }

