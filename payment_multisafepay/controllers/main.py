# Part of Odoo. See LICENSE file for full copyright and licensing details.

import pprint

from odoo import http
from odoo.exceptions import ValidationError
from odoo.http import request

from odoo.addons.payment.logging import get_payment_logger


_logger = get_payment_logger(__name__)


class MultisafepayController(http.Controller):
    _return_url = '/payment/multisafepay/return'
    _webhook_url = '/payment/multisafepay/webhook'

    @http.route(
        _return_url, type='http', auth='public', methods=['GET', 'POST'], csrf=False,
        save_session=False
    )
    def multisafepay_return_from_checkout(self, **data):
        _logger.info("Checkout")
        """Process the payment data sent by Mollie after redirection from checkout.
    
        The route is flagged with `save_session=False` to prevent Odoo from assigning a new session
        to the user if they are redirected to this route with a POST request. Indeed, as the session
        cookie is created without a `SameSite` attribute, some browsers that don't implement the
        recommended default `SameSite=Lax` behavior will not include the cookie in the redirection
        request from the payment provider to Odoo. As the redirection to the '/payment/status' page
        will satisfy any specification of the `SameSite` attribute, the session of the user will be
        retrieved and with it the transaction which will be immediately post-processed.
    
        :param dict data: The payment data (only `id`) and the transaction reference (`ref`)
                          embedded in the return URL.
        """
        _logger.info("handling redirection from MultiSafepay with data:\n%s", pprint.pformat(data))
        self._verify_and_process(data)
        return request.redirect('/payment/status')

    @http.route(_webhook_url, type='http', auth='public', methods=['POST'], csrf=False)
    def multisafepay_webhook(self, **data):
        """Process the payment data sent by Mollie to the webhook.

        :param dict data: The payment data (only `id`) and the transaction reference (`ref`)
                          embedded in the return URL
        :return: An empty string to acknowledge the notification
        :rtype: str
        """
        _logger.info("notification received from MultiSafepay with data:\n%s", pprint.pformat(data))
        self._verify_and_process(data)
        return ''

    @staticmethod
    def _verify_and_process(data):
        _logger.info("verify_and_process")
        """Verify and process the payment data sent by Mollie.

        :param dict data: The payment data.
        :return: None
        """
        # transactionid = data.get('transaction_id')
        # tx_sudo = request.env['payment.transaction'].sudo()._search_by_reference('multisafepay', data)

        tx_sudo = request.env['payment.transaction'].sudo().search([('provider_code','=','multisafepay')],order ='reference desc',limit=1)
        print("tx", tx_sudo)
        if not tx_sudo:
            return

        try:
            # verified_data = tx_sudo._send_api_request(
            #     'GET', f'/orders/{tx_sudo.provider_reference}'
            # )
            verified_data = tx_sudo._send_api_request(
                'GET', f'/orders/{tx_sudo.reference}'
            )
            print('verified_data', verified_data)
            # _logger.info(verified_data)

        except ValidationError:
            _logger.error("Unable to process the payment data")
        else:
            tx_sudo._process('multisafepay', verified_data)

        # tx_sudo = request.env['payment.transaction'].sudo()._search_by_reference(
        #     'flutterwave', data
        # )
        # if not tx_sudo:
        #     return
        #
        # try:
        #     verified_data = tx_sudo._send_api_request(
        #         'GET', 'transactions/verify_by_reference', params={'tx_ref': tx_sudo.reference},
        #     )
        # except ValidationError:
        #     _logger.error("Unable to verify the payment data")
        # else:
        #     tx_sudo._process('flutterwave', verified_data)
        #

