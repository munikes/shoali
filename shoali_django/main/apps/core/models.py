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
    subscribe = models.DateTimeField (auto_now_add=True, default=timezone.now)
    unsubscribe = models.DateTimeField (auto_now=True, default=timezone.now)
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

    def create_shoaliuser (sender, instance, request, **kwargs):
        ShoaliUser.objects.create(user=instance)

    user_registered.connect(create_shoaliuser, sender=User)


class Supply (models.Model):
    UNIT_CHOICES = (
            ('sathosi', 0.00000001),
            ('μBTC', 0.000001),
            ('mBTC', 0.001),
            ('BTC', 1),
            ('kBTC', 1000),
            ('MBTC', 1000000),
            )
    user = models.ManyToManyField(User)
    amount = models.PositiveIntegerField(verbose_name = 'Amount', 
            help_text = 'Indicate amount in .')
    interest = models.PositiveIntegerField(verbose_name = 'Interest', 
            help_text = 'Indicate amount the interest of supply as %', 
            blank = True)
    unit = models.CharField(max_length = 13, choices = UNIT_CHOICES, 
            verbose_name = 'Unit', blank=True)
    description = models.TextField (verbose_name = 'Description', 
            help_text = 'Describe why you want to incur in debt in 140 characters.', 
            blank=True)

    def __unicode__(self):
        return self.amount


class Debt (models.Model):
    UNIT_CHOICES = (
            ('sathosi', 0.00000001),
            ('μBTC', 0.000001),
            ('mBTC', 0.001),
            ('BTC', 1),
            ('kBTC', 1000),
            ('MBTC', 1000000),
            )
    user = models.ManyToManyField(User)
    supply = models.OneToOneField(Supply)
    amount = models.PositiveIntegerField(verbose_name = 'Amount', 
            help_text = 'Indicate amount in .')
    unit = models.CharField(max_length = 13, choices = UNIT_CHOICES, 
            verbose_name = 'Unit', blank=True)
    description = models.TextField (verbose_name = 'Description', 
            help_text = 'Describe why you want to incur in debt in 140 characters.', 
            blank=True)

    def __unicode__(self):
        return self.amount


class Reputation (models.Model):
    user = models.OneToOneField(User)
    amount = models.IntegerField(verbose_name = 'Amount', 
            help_text = 'Indicate amount of kudos.')

    def __unicode__(self):
        return self.amount


class Friend (models.Model):
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.user.nick


class Wallet (models.Model):
    user = models.ForeignKey(User)
    file_wallet = models.FileField(upload_to = 'wallets', verbose_name = 'Wallet', 
            help_text = 'Upload the wallet.dat file', blank=True)

    def __unicode__(self):
        return self.user.name


class BitcoinAddress (models.Model):
    wallet = models.ManyToManyField(Wallet)
    bitcoin_address = models.CharField (max_length = 34, unique = True, 
            verbose_name = 'Bitcoin Address', 
            help_text = 'the bitcoin address (length 27-34)', blank=True)

    def __unicode__(self):
        return self.bitcoin_address


