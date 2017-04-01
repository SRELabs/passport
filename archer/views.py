#!/usr/bin/python
# -*- coding:utf-8 -*-
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from app.models import App
from users.views import check_ticket


@login_required(login_url='/users/login/')
def index(request):
    return render_to_response('base.html', {}, context_instance=RequestContext(request))


@login_required(login_url='/users/login/')
def home(request):
    return render_to_response('home.html', {}, context_instance=RequestContext(request))


def nav(request):
    data = App.objects.all()
    tgc = request.COOKIES.get('ARCHER_TGC', '')
    username = check_ticket(tgc)
    return render_to_response('nav.html', {'data': data, 'username': username},
                              context_instance=RequestContext(request))
