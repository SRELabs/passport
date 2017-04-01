#!/usr/bin/python
# -*- coding:utf-8 -*-
from django.db import models


class Policy(models.Model):
    choice_active = {
        (1, "启用"),
        (2, "禁用")
    }
    choice_default = {
        (2, "子站"),
        (1, "全站")
    }
    policy_id = models.AutoField(primary_key=True)
    policy_name = models.CharField(max_length=50)
    policy_active = models.IntegerField(default=1, choices=choice_active)
    policy_default = models.IntegerField(default=0, choices=choice_default)
    policy_desc = models.CharField(max_length=255, blank=True, null=True, default='')

    def __str__(self):
        return self.policy_id


class PolicyRule(models.Model):
    choice_type = {
        ("all", '所有'),
        ("ip", "ip地址"),
        ("username", "用户名")
    }
    choice_action = {
        ("allow", "允许"),
        ("deny", "拒绝")
    }
    rule_id = models.AutoField(primary_key=True)
    rule_priority = models.IntegerField()
    rule_type = models.CharField(max_length=20, choices=choice_type)
    rule_policy = models.IntegerField()
    rule_action = models.CharField(max_length=10, choices=choice_action)
    rule_value = models.CharField(max_length=50)

    def __str__(self):
        return self.rule_id

    class Meta:
        ordering = ['rule_priority']

