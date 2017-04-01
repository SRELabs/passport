#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from policy.models import PolicyRule, Policy
from app.models import App
import re
from django.contrib import messages
import json


def check_ip(ip):
    p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if p.match(ip):
        return True
    else:
        return False


def check_policy(app_id, username='', ip=''):
    # get policy_id
    msg = {
        'type': 'ip/username',
        'action': 'allow',
        'errmsg': 'nil'
    }
    # common policy
    pr = ''
    try:
        pr = PolicyRule.objects.filter(rule_policy=Policy.objects.get(policy_default=1).policy_id)
    except Exception, e:
        msg['errmsg'] = e.message
    for p in pr:
        if ip and ((p.rule_type == 'ip' and p.rule_value == ip) or p.rule_value == '*'):
            msg['type'] = 'ip'
            if p.rule_action == 'allow':
                msg['action'] = 'Allow'
                return True, msg
            else:
                msg['action'] = 'Deny'
                msg['errmsg'] = ' unauthorized ip！'
                return False, msg
        if username and ((p.rule_type == 'username' and p.rule_value == username) or p.rule_value == '*'):
            msg['type'] = 'username'
            if p.rule_action == 'allow':
                msg['action'] = 'Allow'
                return True, msg
            else:
                msg['action'] = 'Deny'
                msg['errmsg'] = ' unauthorized user！'
            return False, msg
    # service policy
    try:
        pr = PolicyRule.objects.filter(rule_policy=App.objects.get(pk=app_id).app_policy)
    except Exception, e:
        msg['errmsg'] = e.message
    # filter
    for p in pr:
        if ip and ((p.rule_type == 'ip' and p.rule_value == ip) or p.rule_value == '*'):
            msg['type'] = 'ip'
            if p.rule_action == 'allow':
                msg['action'] = 'Allow'
                return True, msg
            else:
                msg['action'] = 'Deny'
                msg['errmsg'] = ' unauthorized ip！'
                return False, msg
        if username and ((p.rule_type == 'username' and p.rule_value == username) or p.rule_value == '*'):
            msg['type'] = 'username'
            if p.rule_action == 'allow':
                msg['action'] = 'Allow'
                return True, msg
            else:
                msg['errmsg'] = ' unauthorized user！'
                msg['action'] = 'Deny'
            return False, msg
    return True, json.dumps(msg, indent=1)


def render_message(request, message_error=False, msg=''):
    if message_error:
        messages.add_message(request, messages.ERROR, msg)
    else:
        messages.add_message(request, messages.SUCCESS, msg)


def paging(page, data, size):
    """
    分页
    :param page:
    :param data:
    :param size:
    :return:
    """
    # 分页----开始
    paginator = Paginator(data, size)
    try:
        data = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        data = paginator.page(1)
        page = 1
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        data = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    # 分页范围
    after_range_num = 5  # 当前页前显示5页
    before_range_num = 4  # 当前页后显示4页
    if page >= after_range_num:
        page_range = paginator.page_range[page - after_range_num:page + before_range_num]
    else:
        page_range = paginator.page_range[0:int(page) + before_range_num]
    # 分页----结束
    return data, page_range
