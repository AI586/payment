# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
import pprint
import werkzeug

from odoo import http
from odoo.http import request
from odoo import api, models, fields, tools, _
_logger = logging.getLogger(__name__)

from odoo.addons.website_sale.controllers.main import WebsiteSale

class checkOutController(http.Controller):
	
	@http.route(['/payment/checkOut/return', '/payment/checkOut/cancel'], type='http', auth='public', website=True, csrf=False)
	def payu_return(self, **post):
		""" checkOut."""
		_logger.info(
			'checkOut: entering form_feedback with post data %s', pprint.pformat(post))
		return_url = '/'
		if post:
			request.env['payment.transaction'].sudo().form_feedback(post, 'checkout_com')
			sale_order_id = request.env['sale.order'].sudo().browse(int(post.get('txnid')))
			transaction = request.env['payment.transaction'].sudo().browse(sale_order_id.payment_tx_id.id)
			payment_token = {
				'name':post.get('tx_id'),
				'partner_id':transaction.partner_id.id,
				'acquirer_id':transaction.acquirer_id.id,
				'acquirer_ref':post.get('csrf_token')
			}
			pay_tok = request.env['payment.token'].sudo().create(payment_token)
			transaction.sudo().write({'state':'done','payment_token_id':pay_tok.id,'acquirer_reference':post.get('csrf_token')})
		return request.redirect('/shop/payment/validate')

class WebsiteSale(WebsiteSale):

	@http.route('/shop/payment/validate', type='http', auth="public", website=True)
	def payment_validate(self, transaction_id=None, sale_order_id=None, **post):
	    if sale_order_id is None:
	    	sale_order_id = request.session.get('sale_order_id')

	    if sale_order_id is None:
	        order = request.website.sale_get_order()
	    else:
	        order = request.env['sale.order'].sudo().browse(sale_order_id)
	        assert order.id == request.session.get('sale_last_order_id')

	    if order:
	        order.with_context(send_email=True).action_confirm()

	    # clean context and session, then redirect to the confirmation page
	    request.website.sale_reset()

	    return request.redirect('/shop/confirmation')