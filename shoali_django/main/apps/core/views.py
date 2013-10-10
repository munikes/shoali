#    This Python file uses the following encoding: utf-8 .
#    See http://www.python.org/peps/pep-0263.html for details

#    Software as a service (SaaS), which allows anyone to manage their money,
#    in the virtual world, transparently, without intermediaries.
#
#    Copyright (C) 2013 Diego Pardilla Mata
#
#    This file is part of Shoali.
#
#    Shoali is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from main.apps.core.forms import BitcoinAddressForm
from main.apps.core.utils import get_blocks, sum_balance
from django.shortcuts import render_to_response
from django.template import RequestContext
import bitcoinrpc


def getbalance (request):
    """
    Get balance of a bitcoin address
    """
    # insert in a config file
    BTC_USER_RPC='mUniKeS'
    BTC_PASSWORD_RPC=''
    BTC_HOST_RPC='agora-2'
    BTC_PORT_RPC=8332
    BTC_HTTPS_RPC=False
    # init variables
    balance = 0
    form_btc = BitcoinAddressForm()
    if request.method == 'POST':
        # get forms
        form_btc = BitcoinAddressForm (request.POST)
        if form_btc.is_valid():
            # connect to bitcoin client
            con_btc = bitcoinrpc.connect_to_remote(BTC_USER_RPC, BTC_PASSWORD_RPC,
                    host=BTC_HOST_RPC, port=BTC_PORT_RPC,use_https=BTC_HTTPS_RPC)
            # get the total number of blocks in this moment
            first_block = 0
            number_blocks = con_btc.getblockcount()
            #first_block = 225990
            #number_blocks = 225990
            bitcoin_entry = get_blocks(con_btc,
                    request.POST.get('bitcoin_address'),first_block,number_blocks)
            balance = sum_balance(con_btc, bitcoin_entry)
    return render_to_response ('query.html', {'form_btc': form_btc,
        'balance':balance}, context_instance = RequestContext(request))
