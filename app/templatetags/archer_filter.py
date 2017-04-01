#!/usr/bin/python
# -*- coding:utf-8 -*-
from django import template
register = template.Library()


@register.filter
def truncate_last(value, arg):
    """
    :return:
    """
    if arg and value:
        r = ''
        for v in value.split('<br>'):
            r = v
        return r
    else:
        return value


@register.filter
def format_status(value, arg):
    """
    暂时未用
    :param value:
    :param arg:
    :return:
    """
    if value == 1:
        return '<span class="label label-sm label-info arrowed">' + arg + '【ID:' + value + '】</span>'
    elif value == 2:
        return '<span class="label label-sm label-info arrowed">' + arg + '【ID:' + value + '】<img height="15" width="15" src="{% static "img/loading.gif"  %}"/> </span>'
    elif value == 3:
        return '<span class="label label-sm label-danger arrowed">' + arg + '【ID:' + value + '】</span>'
    elif value == 4:
        return '<span class="label label-sm label-success arrowed">' + arg + '【ID:' + value + '】</span>'
    else:
        return '<span class="label label-sm label-info arrowed">' + arg + '【ID:' + value + '】</span>'