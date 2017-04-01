#!/usr/bin/python
# -*- coding:utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
                       url(r'^$', 'archer.views.index', name='index'),
                       url(r'^home/$', 'archer.views.home', name='home'),
                       url(r'^nav/$', 'archer.views.nav', name='nav'),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^users/', include('users.urls', namespace='users', app_name='users')),
                       url(r'^app/', include('app.urls', namespace='app', app_name='app')),
                       url(r'^policy/', include('policy.urls', namespace='policy', app_name='policy')),
                       url(r'^system/', include('system.urls', namespace='system', app_name='system')),
                       )
