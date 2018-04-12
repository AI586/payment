odoo.define('payment_checkout.checkout', function(require) {
    "use strict";

    var ajax = require('web.ajax');
    var core = require('web.core');
    var _t = core._t;
    var qweb = core.qweb;
    var int_currencies = [
        'BIF', 'XAF', 'XPF', 'CLP', 'KMF', 'DJF', 'GNF', 'JPY', 'MGA', 'PYGí',
        'RWF', 'KRW', 'VUV', 'VND', 'XOF'
    ];

    $( document ).ready(function() {
        // Open Checkout with further options
        if(!$(this).find('i').length)
            $(this).append('<i class="fa fa-spinner fa-spin"/>');
            $(this).attr('disabled','disabled');

            var $form = $('#payNow').parents('form');
            var acquirer_id = $('#payNow').closest('div.oe_sale_acquirer_button,div.oe_quote_acquirer_button,div.o_website_payment_new_payment');
            acquirer_id = acquirer_id.data('id') || acquirer_id.data('acquirer_id');
            if (! acquirer_id) {
                return false;
        }

        var so_token = $("input[name='token']").val();
        var so_id = $("input[name='return_url']").val().match(/quote\/([0-9]+)/) || undefined;
        if (so_id) {
            so_id = parseInt(so_id[1]);
        }

        var currency = $("input[name='currency']").val();
        var amount = parseFloat($("input[name='amount']").val() || '0.0');
        if (!_.contains(int_currencies, currency)) {
            amount = amount*100;
        }

        ajax.jsonRpc('/shop/payment/transaction/' + acquirer_id, 'call', {
                so_id: so_id,
                so_token: so_token
        });
    });
});
