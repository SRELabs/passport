#!/usr/bin/python
# -*- coding:utf-8 -*-
from django.shortcuts import render_to_response, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib import messages
from policy.forms import *
from library.common import paging, render_message
import re


@login_required(login_url='/system/u/login/')
def policy_list(request):
    page = int(request.REQUEST.get('page', 1))
    data = Policy.objects.all().order_by('policy_id')
    data, page_range = paging(page, data, 400)
    return render_to_response('policy/list.html', {'data': data, 'page_range': page_range},
                              context_instance=RequestContext(request))


@login_required(login_url='/system/u/login/')
def policy_add(request):
    if request.method == 'POST':
        form = PolicyAddForm(request.POST)
        message_error, msg = True, '策略添加s失败'
        if form.is_valid():
            if form.cleaned_data['policy_default'] == 1 and not Policy.objects.filter(policy_default=1):
                if not Policy.objects.filter(policy_name=form.cleaned_data['policy_name']):
                    f = form.save(commit=False)
                    f.save()
                    message_error, msg = False, '策略添加成功'
                else:
                    msg = '策略添加失败，当前策略已经存在'
            else:
                msg = '策略添加失败，只允许存在一条全站策略'
        else:
            msg = '策略添加失败: ' + re.compile(r'<[^>]+>', re.S).sub('', str(form.errors))
        render_message(request, message_error, msg)
    return HttpResponseRedirect(reverse('policy:policy_list'))


@login_required(login_url='/system/u/login/')
def policy_edit(request):
    if request.method == 'POST':
        form = PolicyEditForm(request.POST)
        message_error, msg = False, '修改成功'
        if form.is_valid():
            try:
                p = Policy.objects.get(policy_default__exact=1)
                if form.cleaned_data["policy_default"] == 1 and p.policy_id != form.cleaned_data["policy_id"]:
                    message_error, msg = True, '修改策略失败，只允许存在一条全站策略'
                else:
                    f = form.save(commit=False)
                    f.policy_id = form.cleaned_data["policy_id"]
                    f.save()
            except Policy.DoesNotExist:
                try:
                    if Policy.objects.filter(policy_id=form.cleaned_data["policy_id"]):
                        f = form.save(commit=False)
                        f.policy_id = form.cleaned_data["policy_id"]
                        f.save()
                except Policy.DoesNotExist:
                    message_error, msg = True, '策略不存在，修改失败'
        else:
            message_error, msg = True, 'ERROR: ' + re.compile(r'<[^>]+>', re.S).sub('', str(form.errors))
        render_message(request, message_error, msg)
    return HttpResponseRedirect(reverse('policy:policy_list'))


@login_required(login_url='/system/u/login/')
def policy_del(request, policy_id):
    try:
        p = Policy.objects.get(pk=policy_id)
        # del rule
        PolicyRule.objects.filter(rule_policy=p.policy_id).delete()
        p.delete()
        messages.add_message(request, messages.SUCCESS, '策略删除成功')
    except Policy.DoesNotExist:
        messages.add_message(request, messages.ERROR, '策略不存在，删除失败')
    return HttpResponseRedirect(reverse('policy:policy_list'))


@login_required(login_url='/system/u/login/')
def policy_disable(request, policy_id):
    try:
        p = Policy.objects.get(pk=policy_id)
        p.policy_active = 2
        p.save()
        messages.add_message(request, messages.SUCCESS, '策略禁用成功')
    except Policy.DoesNotExist:
        messages.add_message(request, messages.ERROR, '策略不存在，禁用失败')
    return HttpResponseRedirect(reverse('policy:policy_list'))


@login_required(login_url='/system/u/login/')
def policy_active(request, policy_id):
    try:
        p = Policy.objects.get(pk=policy_id)
        p.policy_active = 1
        p.save()
        messages.add_message(request, messages.SUCCESS, '策略启用成功')
    except Policy.DoesNotExist:
        messages.add_message(request, messages.ERROR, '策略不存在，启用失败')
    return HttpResponseRedirect(reverse('policy:policy_list'))


@login_required(login_url='/system/u/login/')
def policy_rule_list(request, policy_id):
    page = int(request.REQUEST.get('page', 1))
    data = PolicyRule.objects.filter(rule_policy=policy_id).order_by('rule_id')
    policy_name = Policy.objects.get(pk=policy_id).policy_name
    data, page_range = paging(page, data, 400)
    return render_to_response('policy/rule/list.html', {'data': data, 'page_range': page_range, 'policy_id': policy_id,
                                                        'policy_name': policy_name},
                              context_instance=RequestContext(request))


@login_required(login_url='/system/u/login/')
def policy_rule_add(request, rule_policy):
    if request.method == 'POST':
        form = PolicyRuleAddForm(request.POST)
        if form.is_valid():
            if not PolicyRule.objects.filter(rule_policy=rule_policy).filter(
                    rule_value=form.cleaned_data['rule_value']):
                f = form.save(commit=False)
                f.save()
                messages.add_message(request, messages.SUCCESS, '规则添加成功')
                return HttpResponseRedirect(reverse('policy:policy_rule_list', args=[rule_policy]))
            messages.add_message(request, messages.ERROR, '规则添加失败，当前规则已经存在')
        messages.add_message(request, messages.ERROR,
                             'ERROR: ' + re.compile(r'<[^>]+>', re.S).sub('', str(form.errors)))
        return HttpResponseRedirect(reverse('policy:policy_rule_list', args=[rule_policy]))
    else:
        return render_to_response('policy/rule/list.html', {'rule_policy': rule_policy},
                                  context_instance=RequestContext(request))


@login_required(login_url='/system/u/login/')
def policy_rule_edit(request, policy_id):
    if request.method == 'POST':
        msg = '修改成功'
        form = PolicyRuleEditForm(request.POST)
        if form.is_valid():
            if PolicyRule.objects.filter(rule_id=form.cleaned_data["rule_id"]):
                f = form.save(commit=False)
                f.rule_id = form.cleaned_data["rule_id"]
                f.save()
            else:
                msg = '记录不存在!'
            messages.add_message(request, messages.INFO, msg)
        else:
            msg = 'ERROR: ' + re.compile(r'<[^>]+>', re.S).sub('', str(form.errors))
            messages.add_message(request, messages.ERROR, msg)
        return HttpResponseRedirect(reverse('policy:policy_rule_list', args=[policy_id]))
    else:
        messages.add_message(request, messages.ERROR, '请求错误！')
        return HttpResponseRedirect(reverse('policy:policy_rule_list', args=[policy_id]))


@login_required(login_url='/system/u/login/')
def policy_rule_del(request, rule_id):
    policy_id = 0
    try:
        p = PolicyRule.objects.get(pk=rule_id)
        policy_id = p.rule_policy
        p.delete()
        messages.add_message(request, messages.SUCCESS, '删除成功')
    except Policy.DoesNotExist:
        messages.add_message(request, messages.ERROR, '删除失败: 记录不存在')
    if policy_id:
        return HttpResponseRedirect(reverse('policy:policy_rule_list', args=[policy_id]))
    else:
        return HttpResponseRedirect(reverse('policy:policy_list'))
