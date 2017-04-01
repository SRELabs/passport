#!/usr/bin/python
# -*- coding:utf-8 -*-
# from django.contrib.auth.models import User
from rest_framework import serializers
from users.models import *


class TicketSerializer(serializers.Serializer):
    ticket_id = serializers.IntegerField()
    ticket_type = serializers.CharField()
    ticket_value = serializers.CharField()

    def create(self, validated_data):
        return Ticket.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.ticket_value = validated_data.get('ticket_value', instance.ticket_value)
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = (
            'users_name',
            'users_first_name',
            'users_last_name',
            'users_avatar',
            'users_email',
            'users_last_login',
            'users_active'
        )
