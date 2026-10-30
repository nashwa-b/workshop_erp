# Part of Odoo. See LICENSE file for full copyright and licensing details.

# from werkzeug.urls import url_decode, url_parse

from odoo import _,api, models
from odoo.exceptions import ValidationError
from odoo.tools import urls
from odoo.addons.payment import utils as payment_utils

# from odoo.addons.payment.const import CURRENCY_MINOR_UNITS
from odoo.addons.payment.logging import get_payment_logger
from odoo.addons.payment_paypal.const import PAYMENT_STATUS_MAPPING
from odoo.addons.payment_paypal import utils as paypal_utils


# from odoo.addons.payment_mollie import const
# from odoo.addons.payment_mollie.controllers.main import MollieController


_logger = get_payment_logger(__name__)


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    def _get_specific_processing_values(self, processing_values):
        """Override to return specific processing values for MultiSafepay.

        :param processing_values: The generic processing values
        :return: MultiSafepay-specific processing values
        :rtype: dict
        """
        self.ensure_one()

        res = super()._get_specific_processing_values(processing_values)

        if self.provider_code != "multisafepay":
            return res

        _logger.debug("Input processing values: %s", str(processing_values))

        res.update(
            {
                "reference": self.reference,
            }
        )

        _logger.debug("Final processing values: %s", str(res))

        return res

    def _get_specific_rendering_values(self, processing_values):
        """Override to return specific rendering values for MultiSafepay.

        :param processing_values: The generic processing values
        :return: MultiSafepay-specific rendering values
        :rtype: dict
        """
        self.ensure_one()

        res = super()._get_specific_rendering_values(processing_values)

        if self.provider_code != "multisafepay":
            return res

        return processing_values


    def _get_tx_from_notification_data(self, provider_code, notification_data):
        """Override of payment to find the transaction based on MultiSafepay data.

        :param provider_code: The code of the provider that handled the transaction
        :param notification_data: The notification data sent by the provider
        :return: The transaction if found
        :rtype: recordset of `payment.transaction`
        :raises ValidationError: If inconsistent data were received
        :raises ValidationError: If the data match no transaction
        """
        tx = super()._get_tx_from_notification_data(provider_code, notification_data)
        if provider_code != "multisafepay" or len(tx) == 1:
            return tx

        reference = notification_data.get("reference")
        if reference:
            tx = self.search(
                [("reference", "=", reference), ("provider_code", "=", "multisafepay")]
            )

        return tx

    def _paypal_prepare_order_payload(self):
        """ Prepare the payload for the Paypal create order request.

        :return: The requested payload to create a Paypal order.
        :rtype: dict
        """
        partner_first_name, partner_last_name = payment_utils.split_partner_name(self.partner_name)
        if self.partner_id.is_public:
            invoice_address_vals = {'address': {'country_code': self.company_id.country_code}}
            shipping_address_vals = {}
        else:
            invoice_address_vals = paypal_utils.format_partner_address(self.partner_id)
            shipping_address_vals = paypal_utils.format_shipping_address(self)
        shipping_preference = 'SET_PROVIDED_ADDRESS' if shipping_address_vals else 'NO_SHIPPING'

        # See https://developer.paypal.com/docs/api/orders/v2/#orders_create!ct=application/json
        payload = {
            'intent': 'CAPTURE',
            'purchase_units': [
                {
                    'reference_id': self.reference,
                    'description': f'{self.company_id.name}: {self.reference}',
                    'amount': {
                        'currency_code': self.currency_id.name,
                        'value': self.amount,
                    },
                    'payee': {
                        'display_data': {
                            'brand_name': self.provider_id.company_id.name,
                        },
                        'email_address': self.provider_id.paypal_email_account,
                    },
                    **shipping_address_vals,
                },
            ],
            'payment_source': {
                'paypal': {
                    'experience_context': {
                        'shipping_preference': shipping_preference,
                    },
                    'name': {
                        'given_name': partner_first_name,
                        'surname': partner_last_name,
                    },
                    **invoice_address_vals,
                },
            },
        }
        # PayPal does not accept None set to fields and to avoid users getting errors when email
        # is not set on company we will add it conditionally since its not a required field.
        if company_email := self.provider_id.company_id.email:
            payload['purchase_units'][0]['payee']['display_data']['business_email'] = company_email

        return payload

    @api.model
    def _extract_reference(self, provider_code, payment_data):
        """Override of `payment` to extract the reference from the payment data."""
        if provider_code != 'paypal':
            return super()._extract_reference(provider_code, payment_data)
        return payment_data.get('reference_id')

    def _extract_amount_data(self, payment_data):
        """Override of payment to extract the amount and currency from the payment data."""
        if self.provider_code != 'paypal':
            return super()._extract_amount_data(payment_data)

        amount_data = payment_data.get('amount', {})
        amount = amount_data.get('value')
        currency_code = amount_data.get('currency_code')
        return {
            'amount': float(amount),
            'currency_code': currency_code,
        }

    def _apply_updates(self, payment_data):
        """Override of `payment` to update the transaction based on the payment data."""
        if self.provider_code != 'paypal':
            return super()._apply_updates(payment_data)

        if not payment_data:
            self._set_canceled(state_message=_("The customer left the payment page."))
            return

        # Update the provider reference.
        txn_id = payment_data.get('id')
        txn_type = payment_data.get('txn_type')
        if not all((txn_id, txn_type)):
            self._set_error(_(
                "Missing value for txn_id (%(txn_id)s) or txn_type (%(txn_type)s).",
                txn_id=txn_id, txn_type=txn_type
            ))
            return
        self.provider_reference = txn_id
        self.paypal_type = txn_type

        # Force PayPal as the payment method if it exists.
        self.payment_method_id = self.env['payment.method'].search(
            [('code', '=', 'paypal')], limit=1
        ) or self.payment_method_id

        # Update the payment state.
        payment_status = payment_data.get('status')

        if payment_status in PAYMENT_STATUS_MAPPING['pending']:
            self._set_pending(state_message=payment_data.get('pending_reason'))
        elif payment_status in PAYMENT_STATUS_MAPPING['done']:
            self._set_done()
        elif payment_status in PAYMENT_STATUS_MAPPING['cancel']:
            self._set_canceled()
        else:
            _logger.info(
                "Received data with invalid payment status (%s) for transaction %s.",
                payment_status, self.reference
            )
            self._set_error(_("Received data with invalid payment status: %s", payment_status))
