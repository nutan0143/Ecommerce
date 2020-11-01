from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms import ValidationError
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
from .models import *

class UserAuthenticationForm(forms.ModelForm):

    def clean(self):
        email_address = self.cleaned_data.get('email_address')
        password = self.cleaned_data.get('password')
        return super().clean()

    class Meta:
        model = User
        fields = 'email_address', 'password', 'is_active'

class UserSignup(forms.ModelForm):

    def clean(self):
        email_address = self.cleaned_data.get('email_address')
        password = self.cleaned_data.get('password')
        return super().clean()

    class Meta:
        model = User
        fields = 'email_address', 'password', 'is_active','name'

    def save(self):
        import pdb
        pdb.set_trace()
        data= self.instance
        data.is_active = True
        data.set_password(self.data['password'])
        data.save()
        return data