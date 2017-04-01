#!/usr/bin/python
# -*- coding:utf-8 -*-
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
                       # app
                       url(r'^list/$', 'app.views.app_list', name='app_list'),
                       url(r'^add/$', 'app.views.app_add', name='app_add'),
                       url(r'^del/(\d+)$', 'app.views.app_del', name='app_del'),
                       url(r'^edit/$', 'app.views.app_edit', name='app_edit'),
                       url(r'^key_reset/(\d+)$', 'app.views.app_key_reset', name='app_key_reset'),
                       )
