#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from django.conf import settings
from django.http import HttpResponseForbidden
from django.views.debug import technical_500_response

try:
    from django.utils.deprecation import MiddlewareMixin  # Django 1.10.x
except ImportError:
    MiddlewareMixin = object  # Django 1.4.x - Django 1.9.x


class BlockedIpMiddleware(MiddlewareMixin):

    def __init__(self):
        pass

    def process_request(self, request):
        if request.META['REMOTE_ADDR'] in getattr(settings, "BLOCKED_IPS", []):
            return HttpResponseForbidden('<h1>Forbidden</h1>')

    # def process_response(self, request, response):
    #     return None

    def process_exception(self, request, exception):
        if request.user.is_superuser or request.META.get('REMOTE_ADDR') in settings.INTERNAL_IPS:
            return technical_500_response(request, *sys.exc_info())