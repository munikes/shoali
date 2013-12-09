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


from django.forms import ModelForm
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.forms.extras.widgets import SelectDateWidget
import datetime
from decimal import Decimal
from captcha.fields import ReCaptchaField
from registration.forms import RegistrationForm

from main.apps.core.models import ShoaliUser, BitcoinAddress, Loan
from main.apps.core.fields import BCAddressField

# help messages
helps = {
    'birthday': _("Insert your birthday with the format: 'day/month/year'."),
    'telephone': _("Insert your telephone number."),
    'gpg_key': _("Insert your 8 hex digits of your GPG Public KeyID."),
    'first_name': _("Insert your first name. 30 characters or fewer."),
    'last_name': _("Insert your last name or two last names. 60 characters or fewer.")

}
# error messages
errors = {
    'invalid_birthay': _("The format of the birthday must be :"
        "'day/month/year'"),
    'invalid_telephone': _("This value may contain only numbers."),
    'invalid_gpg_key': _("This value may contain only hex digits."),
    'invalid_first_name': _("Your first name have a problem, probably "
            "is longer than 30 characters."),
    'invalid_last_name': _("Your last name have a problem, probably "
            "is longer than 60 characters."),
    'duplicate_gpgkey': _("A user with that GPG KeyID already exists."),
    'duplicate_bitcoinaddress_user': _("You already have this bitcoin "
                    "address inserted."),
}

class ShoaliUserForm (ModelForm):

    birthday = forms.DateField(label=_("Birthday"),
    #        widget=forms.DateInput(format='%d/%m/%Y'),
            input_formats=('%d/%m/%Y',),
            help_text=_(helps['birthday']),
            widget=SelectDateWidget(
                years=range(datetime.datetime.now().year,1913,-1)),
            error_messages={'invalid': _(errors['invalid_birthay'])},
            required=False)
    telephone = forms.RegexField(label=_("Telephone"), max_length=13,
            min_length=9, regex=r'^[\d]+$', help_text = _(helps['telephone']),
            error_messages={
                'invalid': _(errors['invalid_telephone'])},
            required=False)
    gpg_key = forms.RegexField(label=_("GPG Public KeyID"), max_length=8,
            min_length=8, regex=r'^[A-Fa-f0-9]+$',
            help_text=_(helps['gpg_key']),
            error_messages={
                'invalid': _(errors['invalid_gpg_key'])},
            required=False)
    captcha = ReCaptchaField(attrs={'theme' : 'clean'})

    class Meta:
        model = ShoaliUser
        exclude = ('user', 'nick', 'password', 'email','name', 'surname',
                'is_active', 'is_verified', 'is_trusted', 'is_unsubscribe',
                'registration_profile', 'activation_key')

    def clean_gpg_key(self):
        """
        Check if GPG KeyID is null
        """
        gpg_key = self.cleaned_data.get('gpg_key')
        if gpg_key == '':
            gpg_key = None
        return gpg_key


# Add fields of Shoali User in RegistrationForm
RegistrationForm.base_fields.update(ShoaliUserForm.base_fields)
class CustomRegistrationForm (RegistrationForm):
    """
    Form to register User
    """
    first_name = forms.CharField(label=_("First Name"), max_length=30,
            help_text=_(helps['first_name']),
            error_messages={'invalid': _(errors['invalid_first_name'])})
    last_name = forms.CharField(label=_("Last Name"), max_length=60,
            help_text=_(helps['last_name']),
            error_messages={'invalid': _(errors['invalid_last_name'])})

    def __init__(self, *args, **kw):
        super(RegistrationForm, self).__init__(*args, **kw)
        self.fields.keyOrder = ['username', 'password1', 'password2',
                'first_name','last_name', 'gender', 'birthday', 'email',
                'telephone', 'city', 'state', 'country', 'gpg_key',
                'description', 'avatar', 'captcha']

    def clean_gpg_key(self):
        """
        Check if GPG KeyID if is null or duplicate
        """
        gpg_key = self.cleaned_data.get('gpg_key')
        if gpg_key == '':
            gpg_key = None
        else:
            try:
                ShoaliUser.objects.get(gpg_key=gpg_key)
            except ShoaliUser.DoesNotExist:
                return gpg_key
            raise forms.ValidationError(errors['duplicate_gpgkey'])
        return gpg_key


class BitcoinAddressForm (ModelForm):

    bitcoin_address = BCAddressField(max_length=34, min_length=27)
    users = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = BitcoinAddress

    def clean_bitcoin_address(self):
        """
        Check if bitcoin address and user are duplicate
        """
        bitcoin_address = self.cleaned_data.get('bitcoin_address')
        users = self.cleaned_data.get('users')
        try:
            BitcoinAddress.objects.get(users=users, bitcoin_address=bitcoin_address)
        except BitcoinAddress.DoesNotExist:
            return bitcoin_address
        raise forms.ValidationError(errors['duplicate_bitcoinaddress_user'])


class LoanForm (ModelForm):

    UNIT_CHOICES = (
            ('0.00000001', 'sathosi (0.00000001)'),
            ('0.00000100', 'μBTC (0.000001)'),
            ('0.00100000', 'mBTC (0.001)'),
            ('1.00000000', 'BTC (1)'),
            ('1000.00000000', 'kBTC (1000)'),
            ('1000000.00000000', 'MBTC (1000000)'),
            )
    DAYS_CHOICES = (
            (1, 'days'),
            (30, 'month (30 days)'),
            (365, 'years (365 days)'),
            )

    unit = forms.ChoiceField (choices=UNIT_CHOICES, initial='1.00000000')
    days = forms.ChoiceField (choices=DAYS_CHOICES, initial=1)
    interest = forms.DecimalField(min_value=0)
    owner = forms.ModelChoiceField(queryset=ShoaliUser.objects.all(),
            widget=forms.HiddenInput())
    lenders = forms.ModelMultipleChoiceField(queryset=ShoaliUser.objects.all(),
            widget=forms.MultipleHiddenInput(), required=False)
    borrowers = forms.ModelMultipleChoiceField(queryset=ShoaliUser.objects.all(),
            widget=forms.MultipleHiddenInput(), required=False)

    class Meta:
        model = Loan
