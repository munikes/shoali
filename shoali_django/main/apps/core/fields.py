#    This Python file uses the following encoding: utf-8 .
#    See http://www.python.org/peps/pep-0263.html for details

#    Software as a service (SaaS), which allows anyone to manage their money,
#    in the virtual world, transparently, without intermediaries.
#
#    Copyright (C) 2013 Diego Pardilla Mata
#
#    This file is part of Shoali.
#    IMPORTANT: The code of this file has been collected from the
#    bitcointalk.org forum with the topic 'Python code for validating bitcoin 
#    address' with URL: (https://bitcointalk.org/index.php?topic=1026.0), made 
#    by Gavin Andresen (Lead Core Bitcoin Developer), who released the code 
#    into the public domain.
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

import re
from django import forms
from django.forms.util import ValidationError
from django.utils.translation import ugettext_lazy as _
from Crypto.Hash import SHA256

# error messages
errors = {
    'invalid_bitcoinaddress': _("Invalid bitcoin address.")
}

class BCAddressField(forms.CharField):
    """
    Django field type for a Bitcoin Address
    """

    def __init__(self, *args, **kwargs):
        super(BCAddressField, self).__init__(*args, **kwargs)

    def clean(self, value):
        value = value.strip()
        if re.match(r"[a-zA-Z1-9]{27,35}$", value) is None:
            raise ValidationError(errors['invalid_bitcoinaddress'])
        version = get_bcaddress_version(value)
        if version is None:
            raise ValidationError(errors['invalid_bitcoinaddress'])
        return value


__b58chars = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
__b58length = len(__b58chars)

def encode_base58(bc):
    """
    encode bitcoin address which is a string of bytes, to base58.
    """

    long_value = 0L
    for (i, c) in enumerate(bc[::-1]):
        long_value += (256**i) * ord(c)

    result = ''
    while long_value >= __b58length:
        div, mod = divmod(long_value, __b58length)
        result = __b58chars[mod] + result
        long_value = div
    result = __b58chars[long_value] + result

    # Bitcoin does a little leading-zero-compression:
    # leading 0-bytes in the input become leading-1s
    nPad = 0
    for c in bc:
        if c == '\0': nPad += 1
        else: break

    return (__b58chars[0]*nPad) + result

def decode_base58(bc, length):
    """
    decode bitcoin address into a string of len bytes.
    """
    long_value = 0L
    for (i, c) in enumerate(bc[::-1]):
        long_value += __b58chars.find(c) * (__b58length**i)

    result = ''
    while long_value >= 256:
        div, mod = divmod(long_value, 256)
        result = chr(mod) + result
        long_value = div
    result = chr(long_value) + result

    nPad = 0
    for c in bc:
        if c == __b58chars[0]: nPad += 1
        else: break

    result = chr(0)*nPad + result
    if length is not None and len(result) != length:
        return None

    return result

def get_bcaddress_version(strAddress):
    """
    Returns None if strAddress is invalid.
    Otherwise returns integer version of address.
    """
    addr = decode_base58(strAddress,25)
    if addr is None:
        return None
    version = addr[0]
    checksum = addr[-4:]
    vh160 = addr[:-4] # Version plus hash160 is what is checksummed
    h3 = SHA256.new(SHA256.new(vh160).digest()).digest()
    if h3[0:4] == checksum:
        return ord(version)
    return None
