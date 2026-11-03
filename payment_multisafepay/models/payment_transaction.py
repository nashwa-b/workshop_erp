# Part of Odoo. See LICENSE file for full copyright and licensing details.

# from werkzeug.urls import url_decode, url_parse
import requests


from werkzeug.urls import url_decode, url_parse


from odoo.addons.payment_mollie import const

from odoo import _,api, models
from odoo.exceptions import ValidationError
from odoo.tools import urls
from odoo.addons.payment import utils as payment_utils

# from odoo.addons.payment.const import CURRENCY_MINOR_UNITS
from odoo.addons.payment.logging import get_payment_logger
from odoo.addons.payment_paypal.const import PAYMENT_STATUS_MAPPING
from odoo.addons.payment_paypal import utils as paypal_utils
from odoo.addons.payment_mollie import const
from odoo.addons.payment_multisafepay.controllers.main import MultisafepayController
from odoo.addons.payment.const import CURRENCY_MINOR_UNITS




# from odoo.addons.payment_mollie import const
# from odoo.addons.payment_mollie.controllers.main import MollieController


_logger = get_payment_logger(__name__)


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _get_specific_rendering_values(self, processing_values):
        _logger.info("Generated request header..")
        if self.provider_code != 'multisafepay':
            return super()._get_specific_rendering_values(processing_values)

        payload = self._multisafepay_prepare_payment_request_payload()
        try:
            payment_data = self._send_api_request('POST', '/orders', json=payload)
        except ValidationError as error:
            self._set_error(str(error))
            return {}
        self.provider_reference = payment_data.get('id')

        payment_url = payment_data['data']['payment_url']
        parsed_url = url_parse(payment_url)
        url_params = url_decode(parsed_url.query)

        return {
            'api_url': payment_url,
            'url_params': url_params
        }

    def _multisafepay_prepare_payment_request_payload(self):
        _logger.info("Generated payload")

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
            "type": "redirect",
            "gateway": self.payment_method_id.name,
            "order_id": self.reference,
            "currency": self.currency_id.name,
            "amount": int(self.amount * 100),
            "description": self.reference,
            "checkout_options": {"validate_cart": True},
            "customer":{
                'email': self.partner_email,

            },
            "locale": "en_US",
            "payment_options":{
                # "notification_url": self.get_base_url() + "/payment/multisafepay/webhook",
                "webhookUrl": f'{webhook_url}?ref={self.reference}',
                # "notification_method": "POST",

            "redirectUrl": redirect_url,
            # 'webhookUrl': f'{webhook_url}?ref={self.reference}',
            }
        }

    @api.model
    def _extract_reference(self, provider_code, payment_data):
        """Override of `payment` to extract the reference from the payment data."""
        if provider_code != 'multisafepay':
            return super()._extract_reference(provider_code, payment_data)
        return payment_data.get('reference_id')

    def _extract_amount_data(self, payment_data):
        """Override of payment to extract the amount and currency from the payment data."""
        if self.provider_code != 'multisafepay':
            return super()._extract_amount_data(payment_data)

        amount_data = payment_data.get('amount', {})
        amount = amount_data.get('value')
        currency_code = amount_data.get('currency_code')
        return {
            'amount': float(amount),
            'currency_code': currency_code,
        }


    def _apply_updates(self, payment_data):
        _logger.info("status")

        """Override of `payment` to update the transaction based on the payment data."""
        if self.provider_code != 'multisafepay':
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



