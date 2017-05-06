#!/usr/bin/python
# -*- coding:utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('',
                       # user
                       url(r'^registry/$', 'users.views.registry', name='user_registry'),
                       url(r'^login/$', 'users.views.user_login', name='user_login'),
                       url(r'^logout/$', 'users.views.user_logout', name='user_logout'),
                       url(r'^list/$', 'users.views.user_list', name='user_list'),
                       url(r'^add/$', 'users.views.user_add', name='user_add'),
                       url(r'^del/(\w+)/$', 'users.views.user_del', name='user_del'),
                       url(r'^active/(\w+)/$', 'users.views.user_active', name='user_active'),
                       url(r'^edit/$', 'users.views.user_edit', name='user_edit'),
                       url(r'^change_password/$', 'users.views.user_change_password', name='user_change_password'),

                       # API
                       url(r'^api/get_user_info/$', 'users.views.get_user_info'),
                       url(r'^api/auth/$', 'users.views.auth'),

                       )
