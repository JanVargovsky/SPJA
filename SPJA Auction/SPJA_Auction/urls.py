﻿from django.conf.urls import patterns, include, url
from datetime import datetime
from AuctionApp.forms import BootstrapAuthenticationForm, BootstrapUserCreationForm
import AuctionApp.views as views
from django.contrib.auth.views import login
from django.contrib.auth.views import logout
#from django.conf.urls import url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
     # main menu
     url(r'^$', views.home, name='home'),
     url(r'^users/$', views.users, name='users'),
     url(r'^error/$', views.error, name='error'),
     url(r'^userinfo/?(?P<username>\w+)?/?$', views.userinfo, name='userinfo'),
     url(r'^userinfo/(?P<username>\w+)$', views.userinfo, name='userinfo'),
     url(r'^userinfo/edit/(?P<username>\w+)/$', views.userinfoedit, name='userinfoedit'),

     url(r'^items/$', views.useritems, name='useritems'),
     url(r'^item/create/$', views.createitem, name='createitem'),
     url(r'^item/edit/(?P<id>\d+)/$', views.edititem, name='edititem'),
     url(r'^item/delete/(?P<id>\d+)/$', views.deleteitem, name='deleteitem'),

     url(r'^taskstatus/create/$', views.taskstatuscreate, name='taskstatuscreate'),
     url(r'^taskstatus/delete/(?P<id>\d+)/$', views.taskstatusdelete, name='taskstatusdelete'),
     url(r'^taskstatus/list/$', views.taskstatuslist, name='taskstatuslist'),

     url(r'^tasks/list/$', views.taskslist,{'filter': 'notdeleted'}, name='taskslist'),
     url(r'^tasks/list/deleted$', views.taskslist,{'filter': 'deletedonly'}, name='deletedtaskslist'),
     url(r'^tasks/list/all/$', views.taskslist,{'filter': 'all'}, name='alltaskslist'),
     url(r'^tasks/create/$', views.taskcreate, name='taskcreate'),
     url(r'^tasks/edit/(?P<id>\d+)/$', views.taskedit, name='taskedit'),
     url(r'^tasks/delete/(?P<id>\d+)/$', views.taskdelete, name='taskdelete'),

     url(r'^message/send/(?P<username>\w+)/$', views.messagesend, name='messagesend'),
     url(r'^messages/$', views.messagelist, name='messagelist'),
     url(r'^message/delete/(?P<id>\d+)/$', views.messagedelete, name='messagedelete'),
     
     # login
     url(r'^login/$',
        login,
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
        logout,
        {
            'next_page': '/',
        },
        name='logout'),

     # TODO: Create register form...  do it as a last thing, because its
     # complex as fuck
     #register
     #url(r'^register', 'AuctionApp.views.register', name='register'),
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
     url(r'^admin/', include(admin.site.urls)),
     )
