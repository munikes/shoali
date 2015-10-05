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
#    GNU Affero General Public License for more details.$
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from django.conf import settings
from django.contrib.sites.models import Site
from django.contrib.sites.models import RequestSite
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from registration import signals
from registration.models import RegistrationProfile
from registration.views import ActivationView
from registration.views import RegistrationView

from main.apps.core.models import ShoaliUser


class CustomRegistrationView(RegistrationView):

    def register(self, request, form):
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')
        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(request)
        new_user = RegistrationProfile.objects.create_inactive_user(site=site,
                request=request, username=username, email=email, password=password)
        signals.user_registered.send(sender=self.__class__, user=new_user,
                request=request)
        # Customize the register
        user = User.objects.get(username=username)
        shoali_user = ShoaliUser(user=user)
        shoali_user.nick = form.cleaned_data.get('username')
        shoali_user.password = make_password(form.cleaned_data.get('password1'))
        shoali_user.email = form.cleaned_data.get('email')
        registration = RegistrationProfile.objects.get(user=user)
        shoali_user.registration_profile = registration
        shoali_user.activation_key = registration.activation_key
        user.save()
        shoali_user.save()
        return new_user

    def registration_allowed(self, request):
        """
        Indicate whether account registration is currently permitted,
        based on the value of the setting ``REGISTRATION_OPEN``. This
        is determined as follows:

        * If ``REGISTRATION_OPEN`` is not specified in settings, or is
          set to ``True``, registration is permitted.

        * If ``REGISTRATION_OPEN`` is both specified and set to
          ``False``, registration is not permitted.

        """
        return getattr(settings, 'REGISTRATION_OPEN', True)

    def get_success_url(self, request, user):
        """
        Return the name of the URL to redirect to after successful
        user registration.

        """
        return ('registration_complete', (), {})

class CustomActivationView(ActivationView):

    def activate(self, request, activation_key):
        activated = RegistrationProfile.objects.activate_user(activation_key)
        if activated:
            signals.user_activated.send(sender=self.__class__,
                    user=activated,request=request)
            # Customize Shoali User is active field
            shoali_user = ShoaliUser.objects.get(nick=activated)
            shoali_user.is_active = True
            shoali_user.save()
        return activated

    def get_success_url(self, request, user):
        """
        Return the name of the URL to redirect to after successful
        account activation.

        """
        return ('registration_activation_complete', (), {})
