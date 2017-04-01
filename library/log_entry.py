#!/usr/bin/python
# -*- coding:utf-8 -*-
"""
参考server中的写法，步骤。
1、module的class中增加
object_id = 10 # 数字定义一个唯一的值，例如10

2、views.py 之下增加：
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.contrib.contenttypes.models import ContentType
from library.log_entry import process_logs
content_type_id = ContentType.objects.get_for_model(Server).pk
object_id = Server.object_id

3、调用方法
process_logs(request.user.id, content_type_id, object_id, request.user.username, ADDITION, msg)
action_flag对应ADDITION、DELETION、CHANGE
"""
from django.contrib.admin.models import LogEntry


def process_logs(user_id, content_type_id, object_id, username, action_flag, message):
    """
    记录日志
    """
    LogEntry.objects.log_action(
        user_id=user_id,
        content_type_id=content_type_id,
        object_id=object_id,
        object_repr=username,
        action_flag=action_flag,
        change_message=message)
