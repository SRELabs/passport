#!/usr/bin/python
# -*- coding:utf-8 -*-
from django import forms
from users.models import Users


class UserEditForm(forms.Form):
    users_name = forms.CharField(required=True)
    users_password = forms.CharField(required=False)
    users_first_name = forms.CharField(required=False)
    users_last_name = forms.CharField(required=False)
    users_email = forms.EmailField(required=False)


class UserLoginForm(forms.Form):
    users_name = forms.CharField(required=True)
    users_password = forms.CharField(required=True)
    users_otp = forms.IntegerField(required=False)
    next = forms.EmailField(required=False)


class UserChangePasswordForm(forms.Form):
    new_password1 = forms.CharField(required=True)
    new_password2 = forms.CharField(required=True)


class UserRegistryForm(forms.Form):
    users_name = forms.CharField(required=True)
    users_password1 = forms.CharField(required=True, widget=forms.PasswordInput)
    users_password2 = forms.CharField(required=True, widget=forms.PasswordInput)

    def clean(self):
        clean_data = self.cleaned_data
        users_name = clean_data.get('users_name')
        users_password1 = clean_data.get('users_password1')
        users_password2 = clean_data.get('users_password2')
        if not users_password1 or not users_password2:
            raise forms.ValidationError(u'密码不能为空')
        elif users_password1 != users_password2:
            raise forms.ValidationError(_('密码不一致！'), code='invalid')
        return clean_data


class UsersAddForm(forms.ModelForm):
    users_name = forms.CharField(required=True)
    users_password = forms.CharField(required=True)
    users_first_name = forms.CharField(required=False)
    users_last_name = forms.CharField(required=False)
    users_email = forms.EmailField(required=False)
    users_active = forms.IntegerField(required=False)
    users_superuser = forms.IntegerField(required=False)
    users_create_time = forms.DateTimeField(required=False)
    users_last_login = forms.DateTimeField(required=False)

    class Meta:
        model = Users
        fields = '__all__'

    def clean(self):
        cleaned_data = super(UsersAddForm, self).clean()
        users_name = cleaned_data.get('users_name')
        users_password = cleaned_data.get('users_password')
        users_first_name = cleaned_data.get('users_first_name')
        users_last_name = cleaned_data.get('users_last_name')
        users_email = cleaned_data.get('users_email')

        if not users_name:
            self._errors['users_name'] = self.error_class([u"用户名不能为空"])
        if not users_password:
            self._errors['users_password'] = self.error_class([u"密码不能为空"])
        if not users_first_name:
            self._errors['users_first_name'] = self.error_class([u"名不能为空"])
        if not users_last_name:
            self._errors['users_last_name'] = self.error_class([u"姓不能为空"])
        if not users_email:
            self._errors['users_email'] = self.error_class([u"邮箱为空或格式不正确"])
        return cleaned_data


class UsersEditForm(forms.ModelForm):
    users_name = forms.CharField(required=True)
    users_password = forms.CharField(required=False)
    users_first_name = forms.CharField(required=True)
    users_last_name = forms.CharField(required=True)
    users_email = forms.EmailField(required=True)
    users_active = forms.IntegerField(required=False)
    users_superuser = forms.IntegerField(required=False)
    users_create_time = forms.DateTimeField(required=False)
    users_last_login = forms.DateTimeField(required=False)

    class Meta:
        model = Users
        fields = '__all__'

    def clean(self):
        cleaned_data = super(UsersEditForm, self).clean()
        users_name = cleaned_data.get('users_name')
        users_first_name = cleaned_data.get('users_first_name')
        users_last_name = cleaned_data.get('users_last_name')
        users_email = cleaned_data.get('users_email')

        if not users_name:
            self._errors['users_name'] = self.error_class([u"用户名不能为空"])
        if not users_first_name:
            self._errors['users_first_name'] = self.error_class([u"名不能为空"])
        if not users_last_name:
            self._errors['users_last_name'] = self.error_class([u"姓不能为空"])
        if not users_email:
            self._errors['users_email'] = self.error_class([u"邮箱为空或格式不正确"])
        return cleaned_data


class UsersForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = '__all__'

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control col-sm-2', 'required': 'True'}),
            'password': forms.TextInput(attrs={'class': 'form-control', 'type': 'password', 'required': 'True'})
        }
