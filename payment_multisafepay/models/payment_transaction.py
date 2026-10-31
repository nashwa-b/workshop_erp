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
from odoo.addons.payment import const



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
        """Override of `payment` to update the transaction based on MultiSafepay data.

        :param payment_data: The payment data recorded by the MultiSafepay controllers
        :return: None
        """
        self.ensure_one()

        if self.provider_code != "multisafepay":
            super()._apply_updates(payment_data)
            return

        transaction_id = payment_data.get("reference")
        if transaction_id and not self.provider_reference:
            self.provider_reference = transaction_id
            _logger.debug("Updated provider_reference to: %s", transaction_id)

        status = payment_data.get("status")
        # If it's already a native Odoo state, return it directly
        odoo_native_states = [
            "draft",
            "pending",
            "authorized",
            "done",
            "cancel",
            "error",
        ]

        if status in odoo_native_states:
            _logger.debug("Status '%s' is native Odoo state - using as-is", status)
            odoo_state = status
        else:
            odoo_state = self._get_multisafepay_status_to_odoo_state(status)

        if odoo_state == "draft":
            _logger.debug(
                "MSP status '%s' → keeping transaction in draft (ref=%s)",
                status,
                self.reference,
            )

        elif odoo_state == "done":
            _logger.debug(
                "MSP status '%s' → marking transaction done (ref=%s)",
                status,
                self.reference,
            )
            # Fix: Odoo 19 compatibility - _set_done() no longer accepts message parameter
            self._set_done()

        elif odoo_state == "cancel":
            _logger.debug(
                "MSP status '%s' → canceling transaction (ref=%s)",
                status,
                self.reference,
            )
            # Fix: Odoo 19 compatibility - _set_canceled() no longer accepts message parameter
            self._set_canceled()

        elif odoo_state == "error":
            _logger.debug(
                "MSP status '%s' → setting transaction to error (ref=%s)",
                status,
                self.reference,
            )

            self._set_error("Transaction was declined in MultiSafepay.")

        elif odoo_state == "pending":
            _logger.debug(
                "MSP status '%s' → setting transaction to pending (ref=%s)",
                status,
                self.reference,
            )
            # Fix: Odoo 19 compatibility - _set_pending() no longer accepts message parameter
            self._set_pending()

        elif odoo_state == "partial_refunded":
            _logger.debug(
                "MSP status '%s' → payment partially refunded (ref=%s)",
                status,
                self.reference,
            )
            # Fix: Odoo 19 compatibility - _set_done() no longer accepts message parameter
            self._set_done()

        _logger.info("Transaction %s updated to state '%s'", self.reference, odoo_state)

        # def _apply_updates(self, payment_data):
        #     """Override of `payment` to update the transaction based on the payment data."""
        #     if self.provider_code != 'mollie':
        #         return super()._apply_updates(payment_data)
        #
        #     # Update the payment method.
        #     payment_method_type = payment_data.get('method', '')
        #     if payment_method_type == 'creditcard':
        #         payment_method_type = payment_data.get('details', {}).get('cardLabel', '').lower()
        #     payment_method = self.env['payment.method']._get_from_code(
        #         payment_method_type, mapping=const.PAYMENT_METHODS_MAPPING
        #     )
        #     self.payment_method_id = payment_method or self.payment_method_id
        #
        #     # Update the payment state.
        #     payment_status = payment_data.get('status')
        #     if payment_status in ('pending', 'open'):
        #         self._set_pending()
        #     elif payment_status == 'authorized':
        #         self._set_authorized()
        #     elif payment_status == 'paid':
        #         self._set_done()
        #     elif payment_status in ['expired', 'canceled', 'failed']:
        #         self._set_canceled(_("Cancelled payment with status: %s", payment_status))
        #     else:
        #         _logger.info(
        #             "Received data with invalid payment status (%s) for transaction %s.",
        #             payment_status, self.reference
        #         )
        #         self._set_error(_("Received data with invalid payment status: %s.", payment_status))
        #
