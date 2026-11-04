# -*- coding: utf-8 -*-

from werkzeug.urls import url_decode, url_parse
from odoo import api, models
from odoo.exceptions import ValidationError
from odoo.tools import urls
from odoo.addons.payment.logging import get_payment_logger
from odoo.addons.payment_multisafepay.controllers.main import MultisafepayController

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
        base_url = self.provider_id.get_base_url()
        redirect_url = urls.urljoin(base_url, MultisafepayController._return_url)
        webhook_url = urls.urljoin(base_url, MultisafepayController._webhook_url)

        return {
            "type": "redirect",
            "gateway": self.payment_method_id.name,
            "order_id": self.reference,
            "currency": self.currency_id.name,
            "amount": int(self.amount*100),
            "description": self.reference,
            "checkout_options": {"validate_cart": True},
            "customer":{
                'firstname':self.partner_id.name,
                'last_name':self.partner_id.name,
                'address1':self.partner_address,
                'email': self.partner_email,
                'phone1':self.partner_phone
            },
            "locale": "en_US",
            "payment_options":{
                "redirect_url": redirect_url,
            },
                "webhook_url": webhook_url,
        }

    @api.model
    def _extract_reference(self, provider_code, payment_data):
        _logger.info("reference")
        """Override of `payment` to extract the reference from the payment data."""
        if provider_code != 'multisafepay':
            return super()._extract_reference(provider_code, payment_data)
        return payment_data.get('reference_id')

    def _extract_amount_data(self, payment_data):
        _logger.info("amount_data")
        """Override of payment to extract the amount and currency from the payment data."""
        if self.provider_code != 'multisafepay':
            return super()._extract_amount_data(payment_data)

        print("l",payment_data)

        datas = payment_data.get('data')
        print('lkj',datas)

        amount_data = 2000
        data = payment_data.get('data',{})
        amount = data.get('amount')
        am = amount*100
        currency = data.get('currency')
        print("a",amount)

        # currency_code = payment_data.get('currency')
        print("c",currency)
        return {
            'amount': float(am),
            'currency_code': currency,
        }

    def _apply_updates(self, payment_data):
        _logger.info("apply_updates")

        """Override of `payment` to update the transaction based on MultiSafepay data.

        :param payment_data: The payment data recorded by the MultiSafepay controllers
        :return: None
        """
        self.ensure_one()

        if self.provider_code != "multisafepay":
            super()._apply_updates(payment_data)
            return

        status = payment_data.get('data', {}).get('status')

        if status == "initialized":
            _logger.debug(
                "status '%s' → keeping transaction in draft (ref=%s)",
                status,
                self.reference,
            )
        elif status == "completed":
            self._set_done()

        elif status == "cancelled":
            self._set_canceled()

        elif status == "error":
            self._set_error("Transaction was declined in MultiSafepay.")

        elif status == "pending":
            self._set_pending()

        _logger.info("Transaction %s updated to state '%s'", self.reference, status)

        # {'success': True, 'data': {'amount': 2000, 'amount_refunded': 0, 'completed': '2026-11-04T06:06:22', 'costs': [
        #     {'amount': 0.69, 'description': '2.9 % For MasterCard Transactions (min 0.6)', 'transaction_id': 14502368,
        #      'type': 'SYSTEM'}], 'created': '2026-11-04T06:06:22', 'currency': 'USD',
        #                            'custom_info': {'custom_1': None, 'custom_2': None, 'custom_3': None},
        #                            'customer': {'address1': None, 'address2': None, 'city': None, 'cocnumber': None,
        #                                         'company_name': None, 'country': None, 'country_name': None,
        #                                         'email': 'demo@test.com', 'first_name': None, 'house_number': None,
        #                                         'last_name': None, 'locale': 'en_GB', 'phone1': None, 'phone2': None,
        #                                         'state': None, 'zip_code': None}, 'description': 'S01046-11',
        #                            'fastcheckout': 'NO', 'financial_status': 'completed', 'items': None,
        #                            'modified': '2026-11-04T06:06:22', 'order_id': 'S01046-11',
        #                            'payment_details': {'account_holder_name': 'dfcvgb', 'account_id': None,
        #                                                'acquirer_reference_number': '02303636308000000334300',
        #                                                'authorization_code': '006459', 'card_acceptor_id': '100021808',
        #                                                'card_acceptor_location': 'Dummy City',
        #                                                'card_acceptor_name': 'test', 'card_entry_mode': 'UNKNOWN',
        #                                                'card_expiry_date': '2901', 'card_funding': 'C',
        #                                                'card_product': 'MCS', 'card_product_type': 1,
        #                                                'card_program': 'MCC', 'external_transaction_id': '630805032758',
        #                                                'issuer_bin': '550000', 'issuer_country_code': 'KR',
        #                                                'last4': '0004', 'mcc': '1234', 'recurring_flow': None,
        #                                                'recurring_id': None, 'recurring_model': None,
        #                                                'response_code': '00', 'scheme_reference_id': 'MCS060623042',
        #                                                'type': 'MASTERCARD'}, 'payment_methods': [
        #         {'account_holder_name': 'dfcvgb', 'amount': 2000, 'card_expiry_date': '2901', 'currency': 'USD',
        #          'description': 'S01046-11', 'external_transaction_id': '630805032758',
        #          'payment_description': 'MasterCard', 'status': 'completed', 'type': 'MASTERCARD'}],
        #                            'reason': 'Approved or completed successfully', 'reason_code': '1000',
        #                            'related_transactions': None, 'status': 'completed',
        #                            'transaction_id': 1793768782108476, 'var1': None, 'var2': None, 'var3': None}}

