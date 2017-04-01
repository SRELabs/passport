#!/usr/bin/python
# -*- coding:utf-8 -*-
from django.db import models


class App(models.Model):
    app_id = models.AutoField(primary_key=True)
    app_name = models.CharField(max_length=32)
    app_key = models.CharField(max_length=32)
    app_domain = models.CharField(max_length=50)
    app_manager = models.CharField(max_length=20)
    app_callback = models.CharField(max_length=255)
    app_policy = models.IntegerField(default=2)

    def __str__(self):
        return self.app_id


