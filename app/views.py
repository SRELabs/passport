#!/usr/bin/python
# -*- coding:utf-8 -*-
from django.shortcuts import render_to_response, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib import messages
from app.forms import *
from policy.models import Policy
from random import Random
from library.common import paging
import re


def random_str(random_length=32):
    """
    生成随机ST/TGT
    :param random_length:
    :return:
    """
    str1 = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(random_length):
        str1 += chars[random.randint(0, length)]
    return str1


@login_required(login_url='/system/u/login/')
def app_list(request):
    page = int(request.REQUEST.get('page', 1))
    data = App.objects.all().order_by('app_id')
    data, page_range = paging(page, data, 40)
    policy_data = Policy.objects.all()
    return render_to_response('app/list.html', {'data': data, 'policy_data': policy_data, 'page_range': page_range},
                              context_instance=RequestContext(request))


@login_required(login_url='/system/u/login/')
def app_add(request):
    if request.method == 'POST':
        form = AppAddForm(request.POST)
        if form.is_valid():
            if not App.objects.filter(app_domain=form.cleaned_data['app_name']):
                f = form.save(commit=False)
                f.app_key = random_str()
                f.save()
                messages.add_message(request, messages.SUCCESS, '应用添加成功')
                return HttpResponseRedirect(reverse('app:app_list'))
            messages.add_message(request, messages.ERROR, '应用添加失败，当前应用已经存在')
        messages.add_message(request, messages.ERROR, 'ERROR: ' + re.compile(r'<[^>]+>', re.S).sub('', str(form.errors)))
        return HttpResponseRedirect(reverse('app:app_add'))
    else:
        data = Policy.objects.all()
        return render_to_response('app/list.html', {'data': data}, context_instance=RequestContext(request))


@login_required(login_url='/system/u/login/')
def app_edit(request):
    if request.method == 'POST':
        msg = '修改成功'
        form = AppEditForm(request.POST)
        if form.is_valid() and App.objects.filter(app_id=form.cleaned_data['app_id']):
            f = form.save(commit=False)
            f.app_id = form.cleaned_data['app_id']
            f.app_key = App.objects.get(pk=form.cleaned_data['app_id']).app_key
            f.save()
        else:
            msg = '记录不存在或数据异常!'
        messages.add_message(request, messages.INFO, msg)
        return HttpResponseRedirect(reverse('app:app_list'))
    else:
        messages.add_message(request, messages.ERROR, '记录不存在！')
        return HttpResponseRedirect(reverse('app:app_list'))


@login_required(login_url='/system/u/login/')
def app_key_reset(request, app_id):
    try:
        data = App.objects.get(pk=app_id)
        data.app_key = random_str()
        data.save()
        messages.add_message(request, messages.SUCCESS, 'key重置成功！')
    except App.DoesNotExist:
        messages.add_message(request, messages.ERROR, '记录不存在！')
    return HttpResponseRedirect(reverse('app:app_list'))


@login_required(login_url='/system/u/login/')
def app_del(request, app_id):
    try:
        App.objects.get(pk=app_id).delete()
        messages.add_message(request, messages.SUCCESS, '删除成功')
    except App.DoesNotExist:
        messages.add_message(request, messages.ERROR, '记录不存在，删除失败')
    return HttpResponseRedirect(reverse('app:app_list'))
