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
        _logger.info("handling redirection from Mollie with data:\n%s", pprint.pformat(data))
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
        _logger.info("notification received from Mollie with data:\n%s", pprint.pformat(data))
        self._verify_and_process(data)
        return ''


    #
    # @http.route(
    #     _webhook_url,
    #     type='http',
    #     auth='public',
    #     methods=['POST', 'GET'],  # MultiSafepay supports GET but strongly recommends POST
    #     csrf=False
    # )
    # def multisafepay_webhook(self, **kwargs):
    #     """ Process the notification data sent by MultiSafepay via webhook. """
    #     _logger.info("Notification received from MultiSafepay with data:\n%s", pprint.pformat(kwargs))
    #
    #     # 1. Fetch transaction reference/ID from payload (MultiSafepay typically passes transaction_id)
    #     # Adjust 'transaction_id' based on the specific MultiSafepay payload key mapping.
    #     tx_reference = kwargs.get('order_id')
    #
    #     if tx_reference:
    #         # 2. Hand off the data to the standard Odoo payment notification handler
    #         # Odoo automatically searches for the matching payment.transaction record
    #         # and triggers your model's '_process_notification_data' method.
    #         request.env['payment.transaction'].sudo()._handle_notification(
    #             'multisafepay',  # The technical provider name code
    #             kwargs
    #         )
    #
    #     # 3. Return a clean HTTP 200 OK text response to stop MultiSafepay retries
    #     return request.make_response(
    #         "OK",
    #         headers=[('Content-Type', 'text/plain')]
    #     )

    # @http.route(_webhook_url, type='http', methods=['POST'], auth='public', csrf=False)
    # def multisafepay_webhook(self):
    #     _logger.info("Checkout1")
    #
    #     """Process the payment data sent by Xendit to the webhook.
    #
    #     :return: The 'accepted' string to acknowledge the notification.
    #     """
    #     data = request.get_json_data()
    #     _logger.info("Notification received from Xendit with data:\n%s", pprint.pformat(data))
    #
    #     received_token = request.httprequest.headers.get('x-callback-token')
    #     tx_sudo = request.env['payment.transaction'].sudo()._search_by_reference('multisafepay', data)
    #     if tx_sudo:
    #         self._verify_notification_token(received_token, tx_sudo)
    #         tx_sudo._process('multisafepay', data)
    #
    #     return request.make_json_response(['accepted'], status=200)
    #
    # _logger.info("Checkout2")

    # @http.route(_webhook_url,
    #     type="http",
    #     auth="public",
    #     csrf=False,
    #     methods=["POST", "GET"],
    # )
    # def multisafepay_webhook(self, **kwargs):
    #     """Handle MultiSafepay webhook notifications"""
    #
    #     _logger.info("MultiSafepay webhook received via %s", request.httprequest.method)
    #     _logger.debug("MultiSafepay webhook data: %s", str(kwargs))
    #
    #     try:
    #         if request.httprequest.method == "POST":
    #             request.env['payment.transaction'].sudo()._handle_notification('multisafepay', post)
    #             return request.make_response('OK')
    #         else:
    #             request.env['payment.transaction'].sudo()._handle_notification('multisafepay', post)
    #             return request.make_response('OK')
    #     except Exception as e:
    #         _logger.error("Unexpected error in webhook processing: %s", str(e))
    #         return request.make_response("Internal Server Error", status=500)



    # @http.route(_webhook_url, type='http', auth='public', methods=['POST'], csrf=False)
    # def multisafepay_webhook(self, **data):
    #     _logger.info("Webhook")
    #
    #     """Process the payment data sent by Mollie to the webhook.
    #
    #     :param dict data: The payment data (only `id`) and the transaction reference (`ref`)
    #                       embedded in the return URL
    #     :return: An empty string to acknowledge the notification
    #     :rtype: str
    #     """
    #     _logger.info("notification received from MultiSafepay with data:\n%s", pprint.pformat(data))
    #     self._verify_and_process(data)
    #     return ''  # Acknowledge the notification

    @staticmethod
    def _verify_and_process(data):
        _logger.info("verify_and_process")


        print("verify")
        """Verify and process the payment data sent by Mollie.

        :param dict data: The payment data.
        :return: None
        """
        tx_sudo = request.env['payment.transaction'].sudo()._search_by_reference('multisafepay', data)
        if not tx_sudo:
            return

        try:
            verified_data = tx_sudo._send_api_request(
                'GET', f'/payments/{tx_sudo.provider_reference}'
            )
        except ValidationError:
            _logger.error("Unable to process the payment data")
        else:
            tx_sudo._process('multisafepay', verified_data)

