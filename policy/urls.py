#!/usr/bin/python
# -*- coding:utf-8 -*-
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
                       # policy
                       url(r'^$', 'policy.views.policy_list', name='policy_list'),
                       url(r'^add/$', 'policy.views.policy_add', name='policy_add'),
                       url(r'^del/(\d+)$', 'policy.views.policy_del', name='policy_del'),
                       url(r'^disable/(\d+)$', 'policy.views.policy_disable', name='policy_disable'),
                       url(r'^active/(\d+)$', 'policy.views.policy_active', name='policy_active'),
                       url(r'^edit/$', 'policy.views.policy_edit', name='policy_edit'),

                       # # rules
                       url(r'^rule/(\d+)$', 'policy.views.policy_rule_list', name='policy_rule_list'),
                       url(r'^rule/add/(\d+)$', 'policy.views.policy_rule_add', name='policy_rule_add'),
                       url(r'^rule/del/(\d+)$', 'policy.views.policy_rule_del', name='policy_rule_del'),
                       url(r'^rule/edit/(\d+)$', 'policy.views.policy_rule_edit', name='policy_rule_edit'),
                       )
