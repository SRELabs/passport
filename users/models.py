#!/usr/bin/python
# -*- coding:utf-8 -*-
from django.db import models
import hashlib


class Users(models.Model):
    active_status = {
        (0, '已锁定'),
        (1, '已解锁')
    }

    superuser_status = {
        (0, '普通用户'),
        (1, '超级管理员')
    }
    users_name = models.CharField(max_length=20, primary_key=True)
    users_password = models.CharField(max_length=64, null=False, blank=False)
    users_email = models.EmailField(max_length=20, null=False, blank=False)
    users_otp = models.CharField(max_length=32, null=True, blank=True, default='')
    users_first_name = models.CharField(null=True, blank=True, max_length=50, default='')
    users_last_name = models.CharField(null=True, blank=True, max_length=50, default='')
    users_avatar = models.CharField(null=True, blank=True, max_length=50, default='')
    users_active = models.SmallIntegerField(default=1, choices=active_status)
    users_superuser = models.SmallIntegerField(default=0, choices=superuser_status)
    users_create_time = models.DateTimeField()
    users_last_login = models.DateTimeField(null=True, blank=True)
    users_last_login_ip = models.GenericIPAddressField(null=True, blank=True)

    def __str__(self):
        return self.users_name


class Ticket(models.Model):
    ticket_id = models.AutoField(primary_key=True)
    ticket_type = models.CharField(max_length=10, default='TGT')
    ticket_value = models.CharField(max_length=256, null=False, blank=False)
    ticket_username = models.CharField(null=False, blank=False, max_length=50)
    ticket_expires_time = models.DateTimeField()

    def __str__(self):
        return self.ticket_id
