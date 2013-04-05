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

from main.apps.core.forms import UserForm, BitcoinAddressForm
from django.shortcuts import render_to_response
from django.template import RequestContext

def userbitcoin (request):
    # init forms
    form_user = UserForm ()
    form_btc = BitcoinAddressForm ()
    if request.method == 'POST':
        # get forms
        form_user = UserForm(request.POST)
        form_btc = BitcoinAddressForm(request.POST)
        if form_user.is_valid () and form_btc.is_valid():
            # insert user in database
            user = form_user.save()
            # save form bitcoin_address but don't insert in database until get 
            # the foreign key
            bitcoin_address = form_btc.save(commit=False)
            # insert user foreign key in bitcoin table
            bitcoin_address.user = user
            # insert bitcoin address in database
            bitcoin_address.save()
    return render_to_response('test.html', {'form_user': form_user, 
                'form_btc': form_btc}, context_instance = RequestContext(request))
