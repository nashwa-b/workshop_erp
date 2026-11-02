# -*- coding: utf-8 -*-

from odoo import _, fields, models, service, api
from odoo.tools import urls

from odoo.addons.payment.logging import get_payment_logger
from odoo.addons.payment_mollie import const


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

    def _build_request_url(self, endpoint, **kwargs):
        _logger.info("Generated MultiSafepay URL")
        """ Build the MultiSafepay request URL dynamically based on environment state. """
        self.ensure_one()
        if self.state == 'enabled':
            base_url = 'https://api.multisafepay.com/v1/json/'
        else:
            base_url = 'https://testapi.multisafepay.com/v1/json/'

        endpoint = endpoint.lstrip('/')
        return f"{base_url}{endpoint}"

    def _build_request_headers(self, method, endpoint, payload, **kwargs):
        """ Build the headers for the MultiSafepay request. """
        return {
            "accept": "application/json",
            "content-type": "application/json",
            'Authorization': f'Bearer {self.multisafepay_api_key}',
        }

    def _multisafepay_prepare_payment_request_payload(self):
        _logger.info("Generated payload URL")

        """ Create the payload for the payment request based on the transaction values.

        :return: The request payload
        :rtype: dict
        """
        user_lang = self.env.context.get('lang')
        base_url = self.provider_id.get_base_url()
        redirect_url = urls.urljoin(base_url, MultisafepayController._return_url)
        webhook_url = urls.urljoin(base_url, MultisafepayController._webhook_url)
        decimal_places = CURRENCY_MINOR_UNITS.get(
            self.currency_id.name, self.currency_id.decimal_places
        )

        return {
            'description': self.reference,
            'amount': {
                'currency': self.currency_id.name,
                'value': f"{self.amount:.{decimal_places}f}",
            },
            # 'locale': user_lang if user_lang in const.SUPPORTED_LOCALES else 'en_US',
            'method': [const.PAYMENT_METHODS_MAPPING.get(
                self.payment_method_code, self.payment_method_code
            )],
            # Since Mollie does not provide the transaction reference when returning from
            # redirection, we include it in the redirect URL to be able to match the transaction.
            'redirectUrl': f'{redirect_url}?ref={self.reference}',
            'webhookUrl': f'{webhook_url}?ref={self.reference}',
        }

    @api.model
    def _extract_reference(self, provider_code, payment_data):
        """Override of `payment` to extract the reference from the payment data."""
        if provider_code != 'mollie':
            return super()._extract_reference(provider_code, payment_data)
        return payment_data.get('ref')

    def _extract_amount_data(self, payment_data):
        """Override of `payment` to extract the amount and currency from the payment data."""
        if self.provider_code != 'mollie':
            return super()._extract_amount_data(payment_data)

        amount_data = payment_data.get('amount', {})
        amount = amount_data.get('value')
        currency_code = amount_data.get('currency')
        return {
            'amount': float(amount),
            'currency_code': currency_code,
        }

    def _apply_updates(self, payment_data):
        """Override of `payment` to update the transaction based on the payment data."""
        if self.provider_code != 'mollie':
            return super()._apply_updates(payment_data)

        # Update the payment method.
        payment_method_type = payment_data.get('method', '')
        if payment_method_type == 'creditcard':
            payment_method_type = payment_data.get('details', {}).get('cardLabel', '').lower()
        payment_method = self.env['payment.method']._get_from_code(
            payment_method_type, mapping=const.PAYMENT_METHODS_MAPPING
        )
        self.payment_method_id = payment_method or self.payment_method_id

        # Update the payment state.
        payment_status = payment_data.get('status')
        if payment_status in ('pending', 'open'):
            self._set_pending()
        elif payment_status == 'authorized':
            self._set_authorized()
        elif payment_status == 'paid':
            self._set_done()
        elif payment_status in ['expired', 'canceled', 'failed']:
            self._set_canceled(_("Cancelled payment with status: %s", payment_status))
        else:
            _logger.info(
                "Received data with invalid payment status (%s) for transaction %s.",
                payment_status, self.reference
            )
            self._set_error(_("Received data with invalid payment status: %s.", payment_status))


    # import requests
    #
    # url = "https://testapi.multisafepay.com/v1/json/orders?api_key=••••"
    #
    # payload = {
    #     "type": "redirect",
    #     "gateway": "CREDITCARD",
    #     "payment_options": {"close_window": False},
    #     "customer": {
    #         "browser": {},
    #         "locale": "en_US",
    #         "disable_send_email": False
    #     },
    #     "checkout_options": {"validate_cart": False},
    #     "days_active": 30,
    #     "seconds_active": 2592000
    # }
    # headers = {
    #     "accept": "application/json",
    #     "content-type": "application/json"
    # }
    #
    # response = requests.post(url, json=payload, headers=headers)
    #
    # print(response.text)

# def _multisafepay_send_api_request(self, endpoint, payload=None, method='POST'):
    #     """ Custom dispatcher method to execute API requests to MultiSafepay """
    #     url = self._build_request_url(endpoint)
    #     api_key = self.multisafepay_api_key
    #     headers = self._build_request_headers(method, endpoint, payload)
    #
    #     try:
    #         response = requests.request(
    #             method=method,
    #             url=url,
    #             params={'api_key': api_key},
    #             json=payload,
    #             headers=headers,
    #             timeout=60
    #         )
    #
    #         response.raise_for_status()
    #         return response.json()
    #     except requests.exceptions.RequestException as e:
    #         raise ValidationError(f"MultiSafepay API Error: {e}")

    # def _build_request_headers(self, *args, **kwargs):
    #     print("ooooo")
    #     """Override of `payment` to build the request headers."""
    #     if self.code != 'multisafepay':
    #         return super()._build_request_headers(*args, **kwargs)
    #
    #     odoo_version = service.common.exp_version()['server_version']
    #     module_version = self.env.ref('base.module_payment_multisafepay').installed_version
    #     return {
    #         'Accept': 'application/json',
    #         'Authorization': f'Bearer {self.multisafepay_api_key}',
    #         'Content-Type': 'application/json',
    #         # See https://docs.mollie.com/integration-partners/user-agent-strings
    #         'User-Agent': f'Odoo/{odoo_version} MultiSafepayNativeOdoo/{module_version}',
    #     }

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

    # def _build_request_headers(self, *args, **kwargs):
    #     """Override of `payment` to build the request headers."""
    #     if self.code != 'multisafepay':
    #         return super()._build_request_headers(*args, **kwargs)

    #     odoo_version = service.common.exp_version()['server_version']
    #     module_version = self.env.ref('base.module_payment_multisafepay').installed_version
    #     return {
    #         'Accept': 'application/json',
    #         'Authorization': f'Bearer {self.multisafepay_api_key}',
    #         'Content-Type': 'application/json',
    #         # See https://docs.mollie.com/integration-partners/user-agent-strings
    #         'User-Agent': f'Odoo/{odoo_version} MultisafepayNativeOdoo/{module_version}',
    #     }

    # def _parse_response_error(self, response):
    #     """Override of `payment` to parse the error message."""
    #     if self.code != 'multisafepay':
    #         return super()._parse_response_error(response)
    #
    #     return response.json().get('detail', '')

    # def _get_supported_currencies(self):
    #     """ Override of `payment` to return the supported currencies. """
    #     supported_currencies = super()._get_supported_currencies()
    #     if self.code == 'multisafepay':
    #         supported_currencies = supported_currencies.filtered(
    #             lambda c: c.name in const.SUPPORTED_CURRENCIES
    #         )
    #     return supported_currencies
