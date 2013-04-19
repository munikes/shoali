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

class User (models.Model):
    # in the future we will use the user class of Django 
    # that is already implemented.
    name = models.CharField(max_length = 30, verbose_name = 'Name', blank=True)
    surname = models.CharField(max_length = 60, verbose_name = 'Surname', 
            blank=True)
    nick = models.CharField(max_length = 10, verbose_name = 'Nick', unique=True)
    email = models.EmailField(verbose_name = 'e-mail')
    photo = models.ImageField(upload_to = 'photos', verbose_name = 'Photo', 
            blank=True)
    # now is text plain (TODO)
    password = models.CharField(max_length = 128, verbose_name = 'Password')
    country = models.CharField(max_length = 20, verbose_name = 'Country', 
            blank=True)
    state = models.CharField (max_length = 30, verbose_name = 'State', 
            blank=True)
    city = models.CharField (max_length = 30, verbose_name = 'City', blank=True)
    description = models.TextField (verbose_name = 'Description', 
            help_text = 'Describe yourself and your interests in 140 characters.', 
            blank=True)
    public_key = models.CharField (max_length = 8, unique = True, 
            verbose_name = 'GPG Public KeyID', 
            help_text = '8 characters of you GPG Public KeyID.')
    birthday = models.DateField(verbose_name = 'Birthday', blank=True)
    telephone = models.PositiveIntegerField(verbose_name = 'Phone', blank=True)
    GENDER = (
            ('MALE', 'Male'),
            ('FEMALE', 'Female'),
            )
    gender = models.CharField (max_length = 6, choices = GENDER, 
            verbose_name = 'Gender', blank=True)
    subscribe = models.DateField (auto_now_add = True)
    unsubscribe = models.DateField (auto_now = True)
    is_verified = models.BooleanField(default=False)
    # apostille convention
    is_trusted = models.BooleanField(default=False)

    def __unicode__(self):
        return self.nick


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


