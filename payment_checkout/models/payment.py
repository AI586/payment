# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import hashlib
import urlparse
import logging
import requests
import json
from odoo import api, fields, models, _
from odoo.addons.payment.models.payment_acquirer import ValidationError
from odoo.tools.float_utils import float_compare

import logging

_logger = logging.getLogger(__name__)


class PaymentAcquirercheckout_com(models.Model):
	_inherit = 'payment.acquirer'

	provider = fields.Selection(selection_add=[('checkout_com', 'Checkout.com')])
	checkout_merchant_key = fields.Char(string='Secret Key', required_if_provider='checkout_com', groups='base.group_user')
	checkout_merchant_salt = fields.Char(string='Publishable Key', required_if_provider='checkout_com', groups='base.group_user')

	@api.multi
	def checkout_com_form_generate_values(self, values):
		self.ensure_one()
		base_url = self.env['ir.config_parameter'].get_param('web.base.url')
		url = 'https://sandbox.checkout.com/api2/v2/tokens/payment'
		payload ={
			"autoCapTime" : 0,
			"autoCapture" : "N",
			"chargeMode" : "3",
			"currency" : values['currency'] and values['currency'].name or '',
			"value" : values['amount'],
			"customerIp" : "88.215.3.111",
			"description" : "Payment token",
			"metadata" : {
			  "keyName" : "value"
			},
		}
		headers = {
			"authorization": str(self.checkout_merchant_key),
			'content-type': 'application/json'
		}
		r = requests.post(url, data=json.dumps(payload), headers=headers)
		token = r.json()

		sale_order_id = self.env['sale.order'].search([],order='id desc', limit=1)

		token_new = ''
		if token.has_key("id"):
			token_new = token['id']

		checkout_com_values = dict(values,
								key=self.checkout_merchant_salt,
								tx_id=token_new,
								txnid=sale_order_id.id,
								amount=values['amount'],
								productinfo=values['reference'],
								firstname=values.get('partner_name'),
								email=values.get('partner_email'),
								phone=values.get('partner_phone'),
								currencyCode= values['currency'] and values['currency'].name or '',
								currency= values['currency'] and values['currency'].name or '',
								contryCode= values['partner_country'] and values['partner_country'].code or '',
								service_provider='checkout_com',
								)
		return checkout_com_values

