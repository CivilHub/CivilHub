# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
import re

class RegisterForm(forms.Form):
    username = forms.CharField(
        label = 'Email',
        max_length = 32,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'email', 'placeholder': 'Email address'})
    )
    password = forms.CharField(
        label = 'Password',
        max_length = 64,
        widget = forms.PasswordInput(attrs={'class': "form-control", 'id': 'password'})
    )
    passchk = forms.CharField(
        label="Repeat password",
        max_length=32,
        widget=forms.PasswordInput(attrs={'class': "form-control", 'id': 'passchk'})
    )
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(RegisterForm, self).__init__(*args, **kwargs)
        
    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        username = cleaned_data.get('email')
        password = cleaned_data.get('password')
        passchk  = cleaned_data.get('passchk')
        if User.objects.filter(username=username).exists():
            self._errors['email'] = self.error_class(['Email address already taken. Pick another one!'])
            del cleaned_data['email']
        if (password != passchk):
            self._errors['password'] = self.error_class(['Passwords not match!'])
                
        return cleaned_data
        