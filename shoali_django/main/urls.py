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


from django.conf.urls import patterns, include, url
from django.conf import settings
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from main.apps.core.backend.views import CustomRegistrationView, CustomActivationView
from main.apps.core.forms import CustomRegistrationForm
admin.autodiscover()

urlpatterns = patterns('main.apps.core.views',
    # Shoali urls:
    url(r'^$', 'begin', name='begin'),
    url(r'^user/$','user_info', name='user info'),
    url(r'^user/btc$','user_btc_addresses', name='user bitcoin addresses'),
    url(r'^user/lend$','lend_money', name='lend money'),
    # Examples:
    url(r'^balance/$','getbalance', name='balance'),
    url(r'^update_task/$', 'update_task', name='update_task'),
)
urlpatterns += patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # Django regitration enable:
    url(r'^accounts/register/$', CustomRegistrationView.as_view(
        form_class=CustomRegistrationForm),
        name='registration_register'),
    url(r'^accounts/activate/complete/$', direct_to_template,
        {'template': 'registration/activation_complete.html'},
        name='registration_activation_complete'),
    # Activation keys get matched by \w+ instead of the more specific
    # [a-fA-F0-9]{40} because a bad activation key should still get to the view;
    # that way it can return a sensible "invalid key" message instead of a
    # confusing 404.
    url(r'^accounts/activate/(?P<activation_key>\w+)/$', 
        CustomActivationView.as_view(),
        name='registration_activate'),
    url(r'^accounts/', include('registration.backends.default.urls')),
)

# settings DEBUG, serve media files local python server
if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
        }),
    )
