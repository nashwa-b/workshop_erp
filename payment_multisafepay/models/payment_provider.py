# -*- coding: utf-8 -*-

from odoo import fields, models, service
from odoo.tools import urls


import logging
from decimal import Decimal
#
# from payment_multisafepay.sdk import Sdk
# from multisafepay.transport import RequestsTransport

from odoo.addons.payment import const

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

    # def _get_default_payment_method_codes(self):
    #     """ Override of `payment` to return the default payment method codes. """
    #     self.ensure_one()
    #
    #     if self.code != 'mollie':
    #         return super()._get_default_payment_method_codes()
    #     return const.DEFAULT_PAYMENT_METHOD_CODES

        # === REQUEST HELPERS === #
    #
    # def _build_request_url(self, endpoint, **kwargs):
    #     """Override of `payment` to build the request URL."""
    #     if self.code != 'mollie':
    #         return super()._build_request_url(endpoint, **kwargs)
    #     return urls.urljoin('https://api.mollie.com/v2/', endpoint.strip('/'))
    #
    def _build_request_headers(self, *args, **kwargs):
        """Override of `payment` to build the request headers."""
        if self.code != 'multisafepay':
            return super()._build_request_headers(*args, **kwargs)

        odoo_version = service.common.exp_version()['server_version']
        module_version = self.env.ref('base.module_payment_multisafepay').installed_version
        return {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.multisafepay_api_key}',
            'Content-Type': 'application/json',
            # See https://docs.mollie.com/integration-partners/user-agent-strings
            'User-Agent': f'Odoo/{odoo_version} MultisafepayNativeOdoo/{module_version}',
        }

    def _parse_response_error(self, response):
        """Override of `payment` to parse the error message."""
        if self.code != 'multisafepay':
            return super()._parse_response_error(response)

        return response.json().get('detail', '')

    # def _get_supported_currencies(self):
    #     """ Override of `payment` to return the supported currencies. """
    #     supported_currencies = super()._get_supported_currencies()
    #     if self.code == 'multisafepay':
    #         supported_currencies = supported_currencies.filtered(
    #             lambda c: c.name in const.SUPPORTED_CURRENCIES
    #         )
    #     return supported_currencies
