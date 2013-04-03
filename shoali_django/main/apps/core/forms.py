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


from django import forms
from django.forms import ModelForm
from main.apps.core.models import User, BitcoinAddress



class UserForm (ModelForm):
    class Meta:
        model = User


class BitcoinAddressForm (ModelForm):
    bitcoin_address = forms.CharField(max_length = 34, min_length = 27)

    def clean(self):
        """
        Check that the bitcoin address starts with one or three.
        """
        # get bitcoin address from form
        bitcoin_address =  self.cleaned_data.get('bitcoin_address')
        if bitcoin_address and bitcoin_address[0] != '1' and bitcoin_address[0] != '3':
            raise forms.ValidationError('The first digit of a bitcoin address must be either one or three.')

        return self.cleaned_data


    class Meta:
        model = BitcoinAddress
        fields = {'bitcoin_address',}
