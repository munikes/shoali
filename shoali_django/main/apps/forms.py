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


from django.forms import ModelForm
from web_app.models import User
from django.core.validators import validate_email


class LogInForm (ModelForm):
    class Meta:
        model = User
        fields = ('nick', 'password')
        
        
class SignUpForm (ModelForm):
    class Meta:
        model = User
        fields = ('nick', 'password', 'email')
        #widgets = { 'nick': validate_email }
        
        
class NewUserForm (ModelForm):
    class Meta:
        model = User  


