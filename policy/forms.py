#!/usr/bin/python
# -*- coding:utf-8 -*-
from django import forms
from policy.models import Policy, PolicyRule


class PolicyAddForm(forms.ModelForm):
    policy_name = forms.CharField(required=True)
    policy_active = forms.IntegerField(required=True)
    policy_default = forms.IntegerField(required=True)
    policy_desc = forms.CharField(required=False)

    class Meta:
        model = Policy
        fields = '__all__'

        widgets = {
            'policy_name': forms.TextInput(attrs={'class': 'form-control col-sm-2', 'required': 'True'}),
            'policy_active': forms.TextInput(attrs={'class': 'form-control col-sm-2', 'required': 'True'}),
            'policy_default': forms.TextInput(attrs={'class': 'form-control col-sm-2', 'required': 'True'}),
            'policy_desc': forms.TextInput(attrs={'class': 'form-control col-sm-2', 'required': 'False'})
        }

    def clean(self):
        cleaned_data = super(PolicyAddForm, self).clean()
        # policy_id = forms.IntegerField(required=False)
        policy_name = cleaned_data.get('policy_name')
        policy_active = cleaned_data.get('policy_active')
        policy_default = cleaned_data.get('policy_default')
        policy_desc = cleaned_data.get('policy_desc')

        if not policy_name:
            self._errors['policy_name'] = self.error_class([u"请输入应用名称"])
        if not policy_active:
            self._errors['policy_active'] = self.error_class([u"请输入应用名称"])
        # if not policy_id:
        #     self._errors['policy_id'] = self.error_class([u"请输入应用名称"])
        if not policy_default:
            self._errors['policy_default'] = self.error_class([u"请输入应用名称"])
        if not policy_desc:
            self._errors['policy_desc'] = self.error_class([u"请输入应用名称"])
        return cleaned_data


class PolicyEditForm(forms.ModelForm):
    policy_id = forms.IntegerField(required=True)
    policy_name = forms.CharField(required=True)
    policy_active = forms.IntegerField(required=True)
    policy_default = forms.IntegerField(required=True)
    policy_desc = forms.CharField(required=False)

    class Meta:
        model = Policy
        fields = '__all__'

        widgets = {
            'policy_app': forms.TextInput(attrs={'class': 'form-control col-sm-2', 'required': 'True'}),
            'policy_name': forms.TextInput(attrs={'class': 'form-control col-sm-2', 'required': 'True'})
        }

    def clean(self):
        cleaned_data = super(PolicyEditForm, self).clean()
        policy_id = forms.IntegerField(required=True)
        policy_name = cleaned_data.get('policy_name')
        policy_active = cleaned_data.get('policy_active')
        policy_default = cleaned_data.get('policy_default')
        policy_desc = cleaned_data.get('policy_desc')

        if not policy_name:
            self._errors['policy_name'] = self.error_class([u"请输入应用名称"])
        if not policy_active:
            self._errors['policy_active'] = self.error_class([u"请输入应用名称"])
        if not policy_id:
            self._errors['policy_id'] = self.error_class([u"请输入应用名称"])
        if not policy_default:
            self._errors['policy_default'] = self.error_class([u"请输入应用名称"])
        if not policy_desc:
            self._errors['policy_desc'] = self.error_class([u"请输入应用名称"])
        return cleaned_data


class PolicyForm(forms.ModelForm):
    class Meta:
        model = Policy
        fields = '__all__'

        widgets = {
            'policy_app': forms.TextInput(attrs={'class': 'form-control col-sm-2', 'required': 'True'}),
            'policy_name': forms.TextInput(attrs={'class': 'form-control col-sm-2', 'required': 'True'})
        }

    def clean(self):
        cleaned_data = super(PolicyForm, self).clean()
        policy_id = forms.IntegerField(required=True)
        policy_name = cleaned_data.get('policy_name')
        policy_active = cleaned_data.get('policy_active')
        policy_default = cleaned_data.get('policy_default')
        policy_desc = cleaned_data.get('policy_desc')

        if not policy_name:
            self._errors['policy_name'] = self.error_class([u"请输入应用名称"])
        if not policy_active:
            self._errors['policy_active'] = self.error_class([u"请输入应用名称"])
        if not policy_id:
            self._errors['policy_id'] = self.error_class([u"请输入应用名称"])
        if not policy_default:
            self._errors['policy_default'] = self.error_class([u"请输入应用名称"])
        if not policy_desc:
            self._errors['policy_desc'] = self.error_class([u"请输入应用名称"])
        return cleaned_data


class PolicyRuleAddForm(forms.ModelForm):
    rule_priority = forms.IntegerField(required=True)
    rule_type = forms.CharField(required=True)
    rule_policy = forms.IntegerField(required=True)
    rule_action = forms.CharField(required=True)
    rule_value = forms.CharField(required=True)

    class Meta:
        model = PolicyRule
        fields = '__all__'

        widgets = {
            'rule_priority': forms.TextInput(attrs={'class': 'form-control col-sm-2', 'required': 'True'}),
            'rule_type': forms.TextInput(attrs={'class': 'form-control col-sm-2', 'required': 'True'}),
            'rule_policy': forms.TextInput(attrs={'class': 'form-control col-sm-2', 'required': 'True'}),
            'rule_action': forms.TextInput(attrs={'class': 'form-control col-sm-2', 'required': 'True'}),
            'rule_value': forms.TextInput(attrs={'class': 'form-control col-sm-2', 'required': 'True'})
        }

    def clean(self):
        cleaned_data = super(PolicyRuleAddForm, self).clean()
        rule_priority = cleaned_data.get('rule_priority')
        rule_type = cleaned_data.get('rule_type')
        rule_policy = cleaned_data.get('rule_policy')
        rule_action = cleaned_data.get('rule_action')
        rule_value = cleaned_data.get('rule_value')

        if not rule_priority or rule_priority < 1 or rule_priority > 100:
            self._errors['rule_priority'] = self.error_class([u"优先级大于等于1，小于等于100"])
        if not rule_type:
            self._errors['rule_type'] = self.error_class([u"请输入应用名称"])
        if not rule_policy:
            self._errors['rule_policy'] = self.error_class([u"请输入应用名称"])
        if not rule_action:
            self._errors['rule_action'] = self.error_class([u"请输入应用名称"])
        if not rule_value:
            self._errors['rule_value'] = self.error_class([u"请输入应用名称"])
        return cleaned_data


class PolicyRuleEditForm(forms.ModelForm):
    rule_id = forms.IntegerField(required=True)
    rule_priority = forms.IntegerField(required=True)
    rule_type = forms.CharField(required=True)
    rule_policy = forms.IntegerField(required=True)
    rule_action = forms.CharField(required=True)
    rule_value = forms.CharField(required=True)

    class Meta:
        model = PolicyRule
        fields = '__all__'

        widgets = {
            'rule_priority': forms.TextInput(attrs={'class': 'form-control col-sm-2', 'required': 'True'}),
            'rule_type': forms.TextInput(attrs={'class': 'form-control col-sm-2', 'required': 'True'}),
            'rule_policy': forms.TextInput(attrs={'class': 'form-control col-sm-2', 'required': 'True'}),
            'rule_action': forms.TextInput(attrs={'class': 'form-control col-sm-2', 'required': 'True'}),
            'rule_value': forms.TextInput(attrs={'class': 'form-control col-sm-2', 'required': 'True'})
        }

    def clean(self):
        cleaned_data = super(PolicyRuleEditForm, self).clean()
        rule_id = cleaned_data.get('rule_id')
        rule_priority = cleaned_data.get('rule_priority')
        rule_type = cleaned_data.get('rule_type')
        rule_policy = cleaned_data.get('rule_policy')
        rule_action = cleaned_data.get('rule_action')
        rule_value = cleaned_data.get('rule_value')

        if not rule_priority or rule_priority < 1 or rule_priority > 100:
            self._errors['rule_priority'] = self.error_class([u"优先级大于等于1，小于等于100"])
        if not rule_type:
            self._errors['rule_type'] = self.error_class([u"请输入应用名称"])
        if not rule_policy:
            self._errors['rule_policy'] = self.error_class([u"请输入应用名称"])
        if not rule_action:
            self._errors['rule_action'] = self.error_class([u"请输入应用名称"])
        if not rule_id:
            self._errors['rule_id'] = self.error_class([u"请输入应用名称"])
        if not rule_value:
            self._errors['rule_value'] = self.error_class([u"请输入应用名称"])
        return cleaned_data


class PolicyRuleForm(forms.ModelForm):
    class Meta:
        model = PolicyRule
        fields = '__all__'

        widgets = {
            'rule_priority': forms.TextInput(attrs={'class': 'form-control col-sm-2', 'required': 'True'}),
            'rule_type': forms.TextInput(attrs={'class': 'form-control col-sm-2', 'required': 'True'}),
            'rule_policy': forms.TextInput(attrs={'class': 'form-control col-sm-2', 'required': 'True'}),
            'rule_action': forms.TextInput(attrs={'class': 'form-control col-sm-2', 'required': 'True'}),
            'rule_value': forms.TextInput(attrs={'class': 'form-control col-sm-2', 'required': 'True'})
        }

    def clean(self):
        cleaned_data = super(PolicyRuleForm, self).clean()
        rule_id = cleaned_data.get('rule_id')
        rule_priority = cleaned_data.get('rule_priority')
        rule_type = cleaned_data.get('rule_type')
        rule_policy = cleaned_data.get('rule_policy')
        rule_action = cleaned_data.get('rule_action')
        rule_value = cleaned_data.get('rule_value')

        if not rule_priority or rule_priority < 1 or rule_priority > 100:
            self._errors['rule_priority'] = self.error_class([u"优先级大于等于1，小于等于100"])
        if not rule_type:
            self._errors['rule_type'] = self.error_class([u"请输入规则类型"])
        if not rule_policy:
            self._errors['rule_policy'] = self.error_class([u"请输入应用名称"])
        if not rule_action:
            self._errors['rule_action'] = self.error_class([u"请输入应用名称"])
        if not rule_id:
            self._errors['rule_id'] = self.error_class([u"请输入应用名称"])
        if not rule_value:
            self._errors['rule_value'] = self.error_class([u"请输入应用名称"])
        return cleaned_data
