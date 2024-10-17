from django import forms
from django.contrib.auth.forms import UserCreationForm

from propertyapp.models import Login, Tenant, Agent, TenantFeedback, Property


class LoginRegister(UserCreationForm):
    username = forms.CharField()
    password1 = forms.CharField(label="password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="confirm password", widget=forms.PasswordInput)

    class Meta:
        model = Login
        fields = ('username', 'password1', 'password2',)


class TenantRegister(forms.ModelForm):
    class Meta:
        model = Tenant
        fields = '__all__'
        exclude = ('user',)


class AgentRegister(forms.ModelForm):
    class Meta:
        model = Agent
        fields = '__all__'
        exclude = ('user',)


class TenantFeedbackForm(forms.ModelForm):
    class Meta:
        model = TenantFeedback
        fields = ('feedback',)


class ReplyTenantFeedbackForm(forms.ModelForm):
    class Meta:
        model = TenantFeedback
        fields = ('reply',)


class PropertyAgentForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = '__all__'
        exclude = ('agent',)
