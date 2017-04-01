#!/usr/bin/python
# -*- coding:utf-8 -*-
from django import forms
from app.models import App


class AppAddForm(forms.ModelForm):
    app_id = forms.IntegerField(required=False)
    app_name = forms.CharField(required=True)
    app_domain = forms.CharField(required=True)
    app_key = forms.CharField(required=False)
    app_manager = forms.CharField(required=True)
    app_callback = forms.CharField(required=True)

    class Meta:
        model = App
        fields = '__all__'

        widgets = {
            'app_name': forms.TextInput(attrs={'class': 'form-control col-sm-2', 'required': 'True'}),
            'app_domain': forms.TextInput(attrs={'class': 'form-control col-sm-2', 'required': 'True'}),
            'app_manager': forms.TextInput(attrs={'class': 'form-control col-sm-2', 'required': 'True'}),
            'app_callback': forms.TextInput(attrs={'class': 'form-control col-sm-2', 'required': 'True'})
        }

    def clean(self):
        cleaned_data = super(AppAddForm, self).clean()
        app_id = forms.IntegerField(required=True)
        app_name = cleaned_data.get('app_name')
        app_domain = cleaned_data.get('app_domain')
        app_manager = cleaned_data.get('app_manager')
        app_callback = cleaned_data.get('app_callback')

        if not app_name:
            self._errors['app_name'] = self.error_class([u"请输入应用名称"])
        if not app_domain:
            self._errors['app_domain'] = self.error_class([u"请输入应用名称"])
        if not app_manager:
            self._errors['app_manager'] = self.error_class([u"请输入应用名称"])
        if not app_callback:
            self._errors['app_callback'] = self.error_class([u"请输入应用名称"])
        if not app_id:
            self._errors['app_id'] = self.error_class([u"请输入应用名称"])
        return cleaned_data


class AppEditForm(forms.ModelForm):
    app_id = forms.IntegerField(required=True)
    app_name = forms.CharField(required=True)
    app_domain = forms.CharField(required=True)
    app_key = forms.CharField(required=False)
    app_manager = forms.CharField(required=True)
    app_callback = forms.CharField(required=True)

    class Meta:
        model = App
        fields = '__all__'

        widgets = {
            'app_name': forms.TextInput(attrs={'class': 'form-control col-sm-2', 'required': 'True'}),
            'app_domain': forms.TextInput(attrs={'class': 'form-control col-sm-2', 'required': 'True'}),
            'app_manager': forms.TextInput(attrs={'class': 'form-control col-sm-2', 'required': 'True'}),
            'app_callback': forms.TextInput(attrs={'class': 'form-control col-sm-2', 'required': 'True'})
        }

    def clean(self):
        cleaned_data = super(AppEditForm, self).clean()
        app_id = cleaned_data.get('app_id')
        app_name = cleaned_data.get('app_name')
        app_domain = cleaned_data.get('app_domain')
        app_manager = cleaned_data.get('app_manager')
        app_callback = cleaned_data.get('app_callback')
        if not app_id:
            self._errors['app_id'] = self.error_class([u"请输入应用名称"])
        if not app_name:
            self._errors['app_name'] = self.error_class([u"请输入应用名称"])
        if not app_domain:
            self._errors['app_domain'] = self.error_class([u"请输入应用名称"])
        if not app_manager:
            self._errors['app_manager'] = self.error_class([u"请输入应用名称"])
        if not app_callback:
            self._errors['app_callback'] = self.error_class([u"请输入应用名称"])
        return cleaned_data


class AppForm(forms.ModelForm):
    class Meta:
        model = App
        fields = '__all__'

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control col-sm-2', 'required': 'True'}),
            'password': forms.TextInput(attrs={'class': 'form-control', 'type': 'password', 'required': 'True'})
        }

    def clean(self):
        cleaned_data = self.clean()
        app_name = cleaned_data.get('app_name')
        app_domain = cleaned_data.get('app_domain')
        app_manager = cleaned_data.get('app_manager')
        app_callback = cleaned_data.get('app_callback')

        if not app_name:
            self._errors['app_name'] = self.error_class([u"请输入应用名称"])
        if not app_domain:
            self._errors['app_domain'] = self.error_class([u"请输入应用名称"])
        if not app_manager:
            self._errors['app_manager'] = self.error_class([u"请输入应用名称"])
        if not app_callback:
            self._errors['app_callback'] = self.error_class([u"请输入应用名称"])
        return cleaned_data
