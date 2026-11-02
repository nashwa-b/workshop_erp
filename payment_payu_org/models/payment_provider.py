# -*- coding: utf-8 -*-

import hashlib
from urllib.parse import urlencode

from odoo import api, fields, models
from odoo.exceptions import RedirectWarning, ValidationError
from odoo.http import request
from odoo.tools.urls import urljoin

from odoo.addons.payment_payu import const

class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('payu', 'PayU')], ondelete={'payu': 'set default'}
    )

    payu_key_id = fields.Char(string="PayU Key Id", copy=False)
    payu_merchant_salt = fields.Char(
        string="PayU Merchant Salt", copy=False, groups="base.group_system"
    )

    @api.constrains("state")
    def _check_payu_credentials_are_set_before_enabling(self):
        """Check that the PayU credentials are valid when the provider is enabled.

        :raise ValidationError: If the PayU credentials are not set
        """
        for provider in self.filtered(lambda p: p.code == "payu" and p.state != "disabled"):
            if not provider.payu_key_id or not provider.payu_merchant_salt:
                raise ValidationError(
                    self.env._(
                        'PayU credentials are missing. Click the "Connect" button to set up your'
                        " account."
                    )
                )

