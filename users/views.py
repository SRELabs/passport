#!/usr/bin/python
# -*- coding:utf-8 -*-
from django.shortcuts import render_to_response, HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from app.models import *
from users.serializers import *
from users.forms import *
from users.models import *
from library.common import paging, check_policy, render_message
from random import Random
from datetime import datetime
from rest_framework.renderers import JSONRenderer
import hashlib


@require_http_methods(["GET", "POST"])
def registry(request):
    if request.method == 'POST':
        form = UserRegistryForm(request.POST)
        message_error = True
        msg = '用户已经存在'
        if form.is_valid():
            cd = form.cleaned_data
            # 验证密码是否一致
            if cd['users_password1'] == cd['users_password2'] and len(cd['users_password1']) < 6:
                msg = '两次密码不一致或者密码小于6位!'
            else:
                user = Users.objects.filter(users_name=cd['users_name'])
                if not user:
                    m2 = hashlib.md5()
                    m2.update(cd['users_password1'])
                    Users(users_name=cd['users_name'],
                          users_password=m2.hexdigest(), users_create_time=datetime.now(),
                          users_last_login=datetime.now()).save()
                    msg = '注册成功'
                    message_error = False
        else:
            msg = '注册失败: 账户密码不能为空!'
        if message_error:
            messages.add_message(request, messages.ERROR, msg)
            return HttpResponseRedirect(reverse('users:user_registry'))
        else:
            messages.add_message(request, messages.SUCCESS, msg)
            return HttpResponseRedirect(reverse('nav'))
    else:
        return render_to_response('users/register.html', {}, context_instance=RequestContext(request))


@require_http_methods(["GET", "POST"])
def user_login(request):
    # 回调地址
    app_id = request.REQUEST.get('app_id', 0)
    callback = request.REQUEST.get('next', '/')
    message_error = True
    response = HttpResponseRedirect('/nav/')
    try:
        app_obj = App.objects.get(pk=app_id)
    except App.DoesNotExist:
        app_obj = None
    # 登陆请求
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        info = '数据异常,登录失败!'
        if form.is_valid():
            cd = form.cleaned_data
            # check policy
            if request.META.has_key('HTTP_X_FORWARDED_FOR'):
                ip = request.META['HTTP_X_FORWARDED_FOR']
            else:
                ip = request.META['REMOTE_ADDR']
            rs, info = check_policy(app_id, username=cd['users_name'], ip=ip)
            if rs:
                # 验证账号密码
                m2 = hashlib.md5()
                m2.update(cd['users_password'])
                try:
                    user = Users.objects.get(users_name=cd['users_name'], users_password=m2.hexdigest())
                    # ST
                    if user.users_active:
                        if app_obj:
                            archer_st = gen_ticket(user.users_name, ticket_type='ST')
                            response = HttpResponseRedirect(
                                'http://' + app_obj.app_domain + callback + '?st=' + archer_st)
                        else:
                            response = HttpResponseRedirect(reverse('users:user_login') + '?app_id=' + str(app_id))
                        # record last ip
                        Users.objects.filter(users_name=user.users_name).update(users_last_login_ip=ip)
                        # TGT
                        archer_tgt = gen_ticket(user.users_name)
                        response.set_cookie('ARCHER_TGC', archer_tgt, max_age=86400, path='/')
                        message_error, info = False, '登录成功'  # rs
                    else:
                        message_error, info = True, '用户被锁定'
                except Users.DoesNotExist:
                    info = '账号或者密码错误!'
        # 跳转页面
        if message_error:
            messages.add_message(request, messages.ERROR, info)
        return response
    else:
        # 已登录用户
        archer_tgt = request.COOKIES.get('ARCHER_TGC', '')
        username = check_ticket(archer_tgt)

        if username and app_obj:
            if request.META.has_key('HTTP_X_FORWARDED_FOR'):
                ip = request.META['HTTP_X_FORWARDED_FOR']
            else:
                ip = request.META['REMOTE_ADDR']
            rs, info = check_policy(app_obj.app_id, username=username, ip=ip)
            if rs:
                archer_st = gen_ticket(username, ticket_type='ST')
                Users.objects.filter(users_name=username).update(users_last_login_ip=ip)
                response = HttpResponseRedirect('http://' + app_obj.app_domain + callback + '?st=' + archer_st)
                messages.add_message(request, messages.INFO, info)
                return response
            else:
                messages.add_message(request, messages.ERROR, info)
        elif username:
            return HttpResponseRedirect(reverse('nav'))
        # 响应登陆界面
        return render_to_response('users/login.html', {'enable_otp': 0}, context_instance=RequestContext(request))


@require_http_methods(["GET"])
def user_logout(request):
    """
    用户注销
    :param request:
    :return:
    """
    # 来源
    referrer = request.META.get('HTTP_REFERER', '')
    # referrer = request.get_full_path()
    # 删除TGT
    ticket = Ticket.objects.filter(ticket_username=request.user.username)
    ticket.delete()

    # 删除cookie
    response = HttpResponseRedirect(referrer) if referrer else HttpResponseRedirect("/")
    response.delete_cookie('ARCHER_TGC', path='/')

    # 退出
    logout(request)
    return response


# @users_required()
@require_http_methods(["GET", "POST"])
def user_change_password(request):
    """
    修改用户密码
    :param request:
    :return:
    """
    if request.method == 'POST':
        form = UserChangePasswordForm(request.POST)
        message_error = True
        if form.is_valid():
            cd = form.cleaned_data
            # 修改密码
            if cd['new_password1'] != cd['new_password2']:
                msg = "两次密码不一致"
            elif len(cd['new_password1']) < 6:
                msg = "密码必须大于六位"
            elif cd['new_password1'] == cd['new_password2']:
                request.user.set_password(cd['new_password1'])
                request.user.save()
                message_error, msg = False, "修改成功"
            else:
                msg = "未知错误"
        else:
            msg = '密码不允许为空'
        # 前端提示
        render_message(request, message_error, msg)
    return render_to_response('users/change_password.html', {}, context_instance=RequestContext(request))


@login_required(login_url='/system/u/login/')
@require_http_methods(["GET"])
def user_list(request):
    page = int(request.REQUEST.get('page', 1))
    data = Users.objects.all().order_by('users_name')
    data, page_range = paging(page, data, 40)
    return render_to_response('users/list.html', {'data': data, 'page_range': page_range},
                              context_instance=RequestContext(request))


@login_required(login_url='/system/u/login/')
@require_http_methods(["POST"])
def user_add(request):
    form = UsersAddForm(request.POST)
    message_error = True
    msg = '用户已经存在'
    if form.is_valid():
        if not Users.objects.filter(users_name=form.cleaned_data['users_name']):
            m2 = hashlib.md5()
            m2.update(form.cleaned_data['users_password'])
            f = form.save(commit=False)
            f.users_password = m2.hexdigest()
            f.users_create_time = datetime.now()
            f.save()
            msg = '创建成功'
            message_error = False
    else:
        msg = 'ERROR: ' + re.compile(r'<[^>]+>', re.S).sub('', str(form.errors))
    if message_error:
        messages.add_message(request, messages.ERROR, msg)
        return HttpResponseRedirect(reverse('users:user_add'))
    else:
        messages.add_message(request, messages.SUCCESS, msg)
    return HttpResponseRedirect(reverse('users:user_list'))


@login_required(login_url='/system/u/login/')
@require_http_methods(["POST"])
def user_edit(request):
    users_name = request.REQUEST.get('users_name')
    if request.method == 'POST' and users_name:
        message_error, msg = True, '修改失败！'
        try:
            u = Users.objects.get(pk=users_name)
            form_data = UsersEditForm(request.POST or None, instance=u)
            if form_data.is_valid():
                cd = form_data.cleaned_data
                f = form_data.save(commit=False)
                if form_data['users_password']:
                    m2 = hashlib.md5()
                    m2.update(cd['users_password'])
                    f.users_password = m2.hexdigest()
                    f.save()
                    message_error, msg = False, '用户修改成功!'
            else:
                msg = re.compile(r'<[^>]+>', re.S).sub('', str(form_data.errors))
        except Users.DoesNotExist:
            msg = '用户不存在!'
        # 前端提示
        render_message(request, message_error, msg)
    return HttpResponseRedirect(reverse('users:user_list'))


@login_required(login_url='/system/u/login/')
@require_http_methods(["GET"])
def user_del(request, users_name):
    if users_name:
        try:
            users = Users.objects.get(users_name=users_name)
            msg = '用户删除成功！'
            messages.add_message(request, messages.SUCCESS, msg)
            users.delete()
        except Users.DoesNotExist:
            msg = '用户不存在！'
            messages.add_message(request, messages.SUCCESS, msg)
    return HttpResponseRedirect(reverse('users:user_list'))


@login_required(login_url='/system/u/login/')
@require_http_methods(["GET"])
def user_active(request, users_name):
    if users_name:
        try:
            users = Users.objects.get(users_name=users_name)
            if users.users_active == 1:
                users.users_active = 0
                msg = '用户锁定成功！'
            else:
                users.users_active = 1
                msg = '用户解锁成功！'
            users.save()
            messages.add_message(request, messages.SUCCESS, msg)
        except Users.DoesNotExist:
            msg = '用户不存在！'
            messages.add_message(request, messages.SUCCESS, msg)
    return HttpResponseRedirect(reverse('users:user_list'))


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders it's content into JSON.
    """

    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def get_user_info(request):
    """
    通过ST获取用户信息
    :param request:
    :return:
    """
    st = request.REQUEST.get('st', '')
    try:
        ticket_obj = Ticket.objects.get(ticket_value=st, ticket_type='ST')
        try:
            user = Users.objects.get(users_name=ticket_obj.ticket_username)
            serializer = UserSerializer(user)
        except Users.DoesNotExist:
            print 'Not Exists'
    except Ticket.DoesNotExist:
        serializer = UserSerializer()
    return JSONResponse(serializer.data)


@csrf_exempt
def auth(request):
    """验证用户密码，临时用于openvpn"""
    users_name = request.REQUEST.get('users_name', '')
    users_pass = request.REQUEST.get('users_pass', '')
    # 验证账号密码
    m2 = hashlib.md5()
    m2.update(users_pass)
    try:
        user = Users.objects.get(users_name=users_name, users_password=m2.hexdigest())
        if user.users_active:
            ret = 'success'
        else:
            ret = 'fail'
    except Users.DoesNotExist:
        ret = 'fail'
    return HttpResponse(ret)


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


def check_ticket(ticket_value, ticket_type='TGT'):
    if ticket_value:
        try:
            ticket_obj = Ticket.objects.get(ticket_value=ticket_value, ticket_type=ticket_type)
            return ticket_obj.ticket_username
        except Ticket.DoesNotExist:
            return False
    return False


def gen_ticket(username, ticket_type='TGT'):
    """
    生成TGT/ST
    :param ticket_type:
    :param username:
    :return:
    """
    # delete old ticket
    try:
        ticket_obj = Ticket.objects.filter(ticket_username=username).filter(ticket_type=ticket_type)
        ticket_obj.delete()
    except Ticket.DoesNotExist:
        pass
    # gen new ticket
    ticket_value = random_str()
    Ticket(ticket_type=ticket_type, ticket_expires_time=datetime.now(), ticket_username=username,
           ticket_value=ticket_value).save()
    return ticket_value
