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
    nick = models.CharField(max_length = 10, verbose_name = 'Nick', unique=True)
    email = models.EmailField(verbose_name = 'e-mail')

    def __unicode__(self):
        return self.nick


class BitcoinAddress (models.Model):
    user = models.ForeignKey(User)
    bitcoin_address = models.CharField (max_length = 34, unique = True, 
            verbose_name = 'Bitcoin Address', 
            help_text = 'the bitcoin address (length 27-34)', blank=True)

    def __unicode__(self):
        return self.bitcoin_address

