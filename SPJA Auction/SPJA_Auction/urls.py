from django.conf.urls import patterns, include, url
from datetime import datetime
from AuctionApp.forms import BootstrapAuthenticationForm, BootstrapUserCreationForm
import AuctionApp.views as views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
     # main menu
     url(r'^$', views.home, name='home'),
     url(r'^users$', views.users, name='users'),
     url(r'^userinfo$', views.userinfo, name='userinfo'),
     #url(r'^userinfo/(?P<username>\w+)/$', views.userinfo, name='userinfo'),

     # TODO: Create register form...  do it as a last thing, because its
     # complex as fuck
     #url(r'^register', 'AuctionApp.views.register', name='register'),

     # login
     url(r'^login/$',
        'django.contrib.auth.views.login',
        {
            'template_name': 'login.html',
            'authentication_form': BootstrapAuthenticationForm,
            'extra_context':
            {
                'title':'Log in',
            }
        },
        name='login'),
     #logout
    url(r'^logout$',
        'django.contrib.auth.views.logout',
        {
            'next_page': '/',
        },
        name='logout'),
     #register
     #url(r'^register/$',
     #   'registration.forms.RegistrationForm',
     #   {
     #       'template_name': 'register.html',
     #       'form_class': BootstrapUserCreationForm,
     #       'extra_context':
     #       {
     #           'title':'Register',
     #       }
     #   },
     #   name='register'),

    # Uncomment the admin/doc line below to enable admin documentation:
     #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:

     #url(r'^admin/', django.conf.urls.url()),
     url(r'^admin/', include(admin.site.urls)),)
