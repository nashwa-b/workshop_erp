# -*- coding: utf-8 -*-

from odoo import _, fields, models
from odoo.addons.payment.logging import get_payment_logger
from odoo.tools.urls import urljoin


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
        _logger.info("urll")
        """Override of `payment` to build the request URL."""
        if self.code != 'multisafepay':
            return super()._build_request_url(endpoint, **kwargs)

        if self.state == 'enabled':
            api_url = 'https://api.multisafepay.com/v1/json'
        else:
            api_url = 'https://testapi.multisafepay.com/v1/json'

        return urljoin(api_url, endpoint)

    def _build_request_headers(self, method, endpoint, payload, **kwargs):
        _logger.info("headers")
        """ Build the headers for the MultiSafepay request. """
        return {
            "accept": "application/json",
            "content-type": "application/json",
            'Authorization': f'Bearer {self.multisafepay_api_key}',
        }

