#    Description program (TODO)
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
    name = models.CharField(max_length = 30, verbose_name = 'Name', blank=True)
    surname = models.CharField(max_length = 60, verbose_name = 'Surname', blank=True)
    nick = models.CharField(max_length = 10, verbose_name = 'Nick', unique=True)
    email = models.EmailField(verbose_name = 'e-Mail')
    photo = models.ImageField(upload_to = 'photos', verbose_name = 'Photo', blank=True)
    password = models.CharField(max_length = 20, verbose_name = 'Password')
    country = models.CharField(max_length = 20, verbose_name = 'Country', blank=True)
    state = models.CharField (max_length = 30, verbose_name = 'State', blank=True)
    city = models.CharField (max_length = 30, verbose_name = 'City', blank=True)
    description = models.TextField (verbose_name = 'Description', help_text = 'Describe yourself and your interests in 140 characters.', blank=True)
    public_key = models.CharField (max_length = 8, unique = True, verbose_name = 'GPG Public Key', help_text = '8 characters of you GPG Public Key.', blank=True)
    birthday = models.DateField(verbose_name = 'Birthday', blank=True)
    telephone = models.PositiveIntegerField(verbose_name = 'Phone', blank=True)
    GENDER = (
              ('MALE', 'Male'), 
              ('FEMALE', 'Female'),
    )
    gender = models.CharField (max_length = 6, choices = GENDER, verbose_name = 'Gender', blank=True)
    subscribe = models.DateField (auto_now_add = True)
    unsubscribe = models.DateField (auto_now = True)
   
    def __unicode__(self):
        return self.nick


class Profile (models.Model):
    PROFILE_CHOICES = (
        ('MONEYLENDER', 'Moneylender'),
        ('BORROWER', 'Borrower'),
        ('ADMIN', 'Admin'),
        ('USER', 'User'),
    )
    type = models.CharField(max_length = 11, choices = PROFILE_CHOICES)
    user_id = models.ForeignKey(User)
    
    def __unicode__(self):
        return self.type
    
    
class Supply (models.Model):
    UNIT_CHOICES = (
        ('UNIT', 1),
        ('THOUSAND', 1000),
        ('MILLION', 1000000),
        ('BILLION', 1000000000),
    )
    user_id = models.ManyToManyField(User)
    amount = models.PositiveIntegerField(verbose_name = 'Amount', help_text = 'Indicate amount in €.')
    unit = models.CharField(max_length = 13, choices = UNIT_CHOICES, verbose_name = 'Unit', blank=True)
    description = models.TextField (verbose_name = 'Description', help_text = 'Describe why you want to incur in debt in 140 characters.', blank=True)
    
    def __unicode__(self):
        return self.amount
    
    
class Debt (models.Model):
    UNIT_CHOICES = (
        ('UNIT', 1),
        ('THOUSAND', 1000),
        ('MILLION', 1000000),
        ('BILLION', 1000000000),
    )
    user_id = models.ManyToManyField(User)
    supply_id = models.OneToOneField(Supply)
    amount = models.PositiveIntegerField(verbose_name = 'Amount', help_text = 'Indicate amount in €.')
    unit = models.CharField(max_length = 13, choices = UNIT_CHOICES, verbose_name = 'Unit', blank=True)
    description = models.TextField (verbose_name = 'Description', help_text = 'Describe why you want to incur in debt in 140 characters.', blank=True)
    
    def __unicode__(self):
        return self.amount
    
class Money (models.Model):
    bitcoin = models.BigIntegerField(primary_key=True)
    user_id = models.OneToOneField(User)
    amount = models.PositiveIntegerField(verbose_name = 'Amount', help_text = 'Indicate amount in €.')
    
    def __unicode__(self):
        return self.amount
    
    
class Reputation (models.Model):
    user_id = models.OneToOneField(User)
    amount = models.PositiveIntegerField(verbose_name = 'Amount', help_text = 'Indicate amount of kudos.')
    
    def __unicode__(self):
        return self.amount
    

class Friend (models.Model):
    user_id = models.ForeignKey(User)
    
    def __unicode__(self):
        return self.user_id.name
    

class Interest (models.Model):
    sale_id = models.OneToOneField(Supply)
    amount = sale_id.amount * models.PositiveIntegerField(verbose_name = 'Amount', help_text = 'Indicate amount the interest of supply as %.')
    
    def __unicode__(self):
        return self.amount
    
    