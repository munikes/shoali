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


from django import get_version
from django.conf.urls import patterns, include, url
from django.conf import settings
from django.views.generic import TemplateView
from django.core.urlresolvers import reverse_lazy

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from main.apps.core.backend.views import CustomRegistrationView, CustomActivationView
from main.apps.core.forms import CustomRegistrationForm
from distutils.version import LooseVersion
admin.autodiscover()

from main.apps.core import views

urlpatterns = patterns('main.apps.core.views',
    # Shoali urls:
    url(r'^$', views.BeginView.as_view(), name='begin'),
    url(r'^btc/$',
        login_required(views.BitcoinAddressList.as_view()), name='btc_list'),
    url(r'^btc/new/$',
        login_required(views.BitcoinAddressCreate.as_view()), name='btc_new'),
    url(r'^btc/edit/(?P<pk>\d+)$',
        login_required(views.BitcoinAddressUpdate.as_view()), name='btc_edit'),
    url(r'^btc/delete/(?P<pk>\d+)$',
        login_required(views.BitcoinAddressDelete.as_view()), name='btc_delete'),
    url(r'^btc/delete_list/$',
        login_required(views.BitcoinAddressDeleteList.as_view()),
        name='btc_delete_list'),
    url(r'^loan/$',
        login_required(views.LoanList.as_view()), name='loan_list'),
    url(r'^loan/new_lend/$',
        login_required(views.LendCreate.as_view()), name='lend_new'),
    url(r'^loan/new_borrow/$',
        login_required(views.BorrowCreate.as_view()), name='borrow_new'),
    url(r'^loan/edit/(?P<pk>\d+)$',
        login_required(views.LoanUpdate.as_view()), name='loan_edit'),
    url(r'^loan/delete/(?P<pk>\d+)$',
        login_required(views.LoanDelete.as_view()), name='loan_delete'),
    url(r'^loan/delete_list/$',
        login_required(views.LoanDeleteList.as_view()),
        name='loan_delete_list'),
    url(r'^user/$','user_info', name='user info'),
    url(r'^user/btc$','user_btc_addresses', name='user bitcoin addresses'),
    url(r'^user/btc/(?P<id>\d+)$','user_btc_addresses', name='edit user bitcoin addresses'),
    url(r'^user/loan$','do_loan', name='do loan'),
    url(r'^user/loan/(?P<id>\d+)$','do_loan', name='edit loan'),
    # Examples:
    url(r'^balance/$','getbalance', name='balance'),
    url(r'^update_task/$', 'update_task', name='update_task'),
)
if (LooseVersion(get_version()) >= LooseVersion('1.6')):
    urlpatterns += patterns('',
                            url(r'^accounts/password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
                                auth_views.password_reset_confirm,
                            {'post_reset_redirect': reverse_lazy('password_reset_complete'),
                               'template_name': 'registration/reset_password_confirm.html'},
                                name='password_reset_confirm')
                        )
else:
    urlpatterns += patterns('',
                            url(r'^accounts/password/reset/confirm/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
                                auth_views.password_reset_confirm,
                            {'post_reset_redirect': reverse_lazy('password_reset_complete'),
                               'template_name': 'registration/reset_password_confirm.html'},
                                name='password_reset_confirm')
                        )
urlpatterns += patterns('',
    url(r'^password/reset/$', auth_views.password_reset,
        {'post_reset_redirect': reverse_lazy('password_reset_done'),
        'template_name': 'registration/reset_password_form.html',
        'email_template_name':'registration/reset_password_email.html',
        'subject_template_name':'registration/password_reset_subject.txt'},
        name='password_reset'),
    url(r'^password/reset/complete/$', auth_views.password_reset_complete,
        {'template_name': 'registration/reset_password_complete.html'},
        name='password_reset_complete'),
    url(r'^password/reset/done/$', auth_views.password_reset_done,
        {'template_name': 'registration/reset_password_done.html'},
        name='password_reset_done'),
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # Django regitration enable:
    url(r'^accounts/register/$', CustomRegistrationView.as_view(
        form_class=CustomRegistrationForm),
        name='registration_register'),
    url(r'^accounts/activate/complete/$',
        TemplateView.as_view(template_name='registration/activation_complete.html'),
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

# if settings DEBUG, serve media files local python server
if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
        }),
    )

