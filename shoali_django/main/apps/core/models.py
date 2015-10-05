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

import logging
logger = logging.getLogger(__name__)
from decimal import Decimal
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from registration.models import RegistrationProfile
from registration.signals import user_registered

class ShoaliUser (models.Model):

    # Related Shoali User with Django User
    user = models.OneToOneField(User)
    # User (duplicated inform in user django auth module, fields (nick, name,
    # surname, password and email))
    nick = models.CharField(max_length=30, verbose_name='Username', unique=True)
    password = models.CharField(max_length=128, verbose_name='Password')
    name = models.CharField(max_length=30, verbose_name='Name', blank=True)
    surname = models.CharField(max_length=60, verbose_name='Surname',
                    blank=True)
    email = models.EmailField(verbose_name='e-mail')
    # relative directories (unique nick name)
    def avatars_to(instance, filename):
        """
        Create relative path with nick and filename p.e 'avatars/nick/filename'
        """
        # TODO: this path in config file
        return 'avatars/%s/%s' % (instance.nick, filename)
    avatar = models.ImageField(upload_to=avatars_to, verbose_name='Avatar',
            blank=True)
    country = models.CharField(max_length=20, verbose_name='Country',
            blank=True)
    state = models.CharField (max_length=30, verbose_name='State',
            blank=True)
    city = models.CharField (max_length=30, verbose_name='City', blank=True)
    description = models.TextField (verbose_name='Description',
            help_text='Describe yourself and your interests in 140 characters.',
            blank=True)
    gpg_key = models.CharField (max_length=8, unique=True,
            verbose_name='GPG Public KeyID', null=True,
            help_text='8 characters of you GPG Public KeyID.')
    birthday = models.DateField(verbose_name='Birthday', null=True)
    telephone = models.CharField(max_length=13, verbose_name='Phone', blank=True)
    GENDER = (
            ('MALE', 'Male'),
            ('FEMALE', 'Female'),
            )
    gender = models.CharField (max_length=6, choices=GENDER,
            verbose_name='Gender', blank=True)
    is_active = models.BooleanField (default=False)
    subscribe = models.DateTimeField (auto_now_add=True)
    unsubscribe = models.DateTimeField (auto_now_add=True)
    is_unsubscribe = models.BooleanField (default=False)
    is_verified = models.BooleanField(default=False)
    # apostille convention
    is_trusted = models.BooleanField(default=False)
    # Related Shoali Registration Profile with Registration Profile
    registration_profile = models.OneToOneField(RegistrationProfile)
    # Registration Key (duplicated inform in registration module)
    activation_key = models.CharField(max_length=40)
    friends = models.ManyToManyField('self', blank=True)

    def __unicode__(self):
        return self.nick

    def create_shoaliuser (self, sender, instance, request, **kwargs):
        ShoaliUser.objects.create(user=instance)

    user_registered.connect(create_shoaliuser, sender=User)


class Loan (models.Model):

    UNIT_CHOICES = (
            (Decimal('0.00000001'), 'sathosi (0.00000001)'),
            (Decimal('0.000001'), 'μBTC (0.000001)'),
            (Decimal('0.001'), 'mBTC (0.001)'),
            (Decimal('1'), 'BTC (1)'),
            (Decimal('1000'), 'kBTC (1000)'),
            (Decimal('1000000'), 'MBTC (1000000)'),
            )
    DAYS_CHOICES = (
            (1, 'days'),
            (30, 'month (30 days)'),
            (365, 'years (365 days)'),
            )
    owner = models.ForeignKey(ShoaliUser)
    borrowers = models.ManyToManyField(ShoaliUser, related_name="borrowers",
            blank=True)
    lenders = models.ManyToManyField(ShoaliUser, related_name="lenders",
            blank=True)
    amount = models.DecimalField(verbose_name='Amount', max_digits=20, 
            decimal_places=8, help_text='Indicate amount.')
    interest = models.DecimalField(verbose_name='Interest', max_digits=6,
            decimal_places=3,
            help_text='Indicate amount the interest of supply as %.')
    unit = models.DecimalField(choices=UNIT_CHOICES,
            max_digits=15, verbose_name='Unit', decimal_places=8)
    description = models.TextField (verbose_name='Description',
            help_text='Describe your main motivations.',
            blank=True)
    period = models.PositiveIntegerField(verbose_name='Period',
            help_text='Indicate repayment period.')
    days = models.PositiveIntegerField(choices=DAYS_CHOICES, verbose_name='Days')

    def _get_total_amount(self):
        return (self.amount * self.unit) * self.interest/Decimal('100') + (self.amount * self.unit)
    total_amount = property(_get_total_amount)

    def _get_total_days(self):
        return self.period * self.days
    total_days = property(_get_total_days)

#    TODO: I don't know why not put this exception, problem with the m2m fields
#    def save(self, *args, **kwargs):
#        if self.lenders == 'blank' and self.borrowers == 'blank':
#            raise Exception('It is possible that there is neither a loan \
#lenders or borrowers')
#        else:
#            super(Loan, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'amount: %s %s - repayment period: %s %s - borrowers:[%s] and \
lenders:[%s] - interest: %s %%' % (self.amount, self.unit, self.period, self.days,
                    self.borrowers, self.lenders, self.interest)


class Reputation (models.Model):

    user = models.OneToOneField(ShoaliUser)
    amount = models.IntegerField(verbose_name='Amount',
            help_text='Indicate amount of kudos.')

    def __unicode__(self):
        return self.amount


# Was thought handle files wallet.dat, but can be a problem because
# you have to guard them, and really do not serve for the proper functioning 
# of the application
#class Wallet (models.Model):
#    user = models.ForeignKey(ShoaliUser)
#    file_wallet = models.FileField(upload_to='wallets', verbose_name='Wallet',
#            help_text='Upload the wallet.dat file', blank=True)
#
#    def __unicode__(self):
#        return self.user.name


class BitcoinAddress (models.Model):
#    wallets = models.ManyToManyField(Wallet)
#    users = models.ManyToManyField(ShoaliUser,
#            through = 'BitcoinAddress_ShoaliUser', symmetrical=False,)
    users = models.ManyToManyField(ShoaliUser)
    bitcoin_address = models.CharField (max_length=34, unique=True,
            verbose_name='Bitcoin Address',
            help_text='the bitcoin address (length 27-34).')

    def __unicode__(self):
        return self.bitcoin_address
