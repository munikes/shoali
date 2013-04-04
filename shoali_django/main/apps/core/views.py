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

from main.apps.core.forms import BitcoinAddressForm, RPCConnectForm
from django.shortcuts import render_to_response
from django.template import RequestContext
from bitcoinrpc.authproxy import AuthServiceProxy as ServiceProxy
import socket


def getbalance (request):
    user_RPC = 'user'
    passwd_RPC = 'password'
    if request.method == 'POST':
        # get form
        form_url = RPCConnectForm (request.POST)
        form_btc = BitcoinAddressForm (request.POST)
        if form_url.is_valid() and form_btc.is_valid():
            con = ServiceProxy ('http://%s:%s@%s:%d' % (user_RPC, passwd_RPC, 
                socket.gethostbyname(form_url.cleaned_data['host']), 
                form_url.cleaned_data['port']))
            account = con.getaccount(form_btc.cleaned_data['bitcoin_address'])
            balance = con.getbalance(account)
            return render_to_response ('query.html', {'balance':balance}, 
                    context_instance = RequestContext(request))
        else:
            return render_to_response ('query.html', {'form_url': form_url, 
                'form_btc': form_btc}, context_instance = RequestContext(request))
    else:
        form_url = RPCConnectForm()
        form_btc = BitcoinAddressForm()
        return render_to_response('query.html', {'form_url': form_url, 
            'form_btc': form_btc}, context_instance = RequestContext(request))

