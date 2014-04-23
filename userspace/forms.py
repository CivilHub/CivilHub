# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
import re

class RegisterForm(forms.Form):
    username = forms.CharField(
        label = 'Username',
        max_length = 32,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'username', 'placeholder': 'Username'})
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
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        passchk  = cleaned_data.get('passchk')
        if User.objects.filter(username=username).exists():
            self._errors['username'] = self.error_class(['Username already taken. Pick another one!'])
            del cleaned_data['username']
        else:
            if username != re.sub('[^a-zA-Z0-9 ]', '', username):
                self._errors['username'] = self.error_class(['Please, use just characters from range [A-Za-z0-9 ]!'])
            if len(username) < 3:
                self._errors['username'] = self.error_class(['Username too short'])
        if (password != passchk):
            self._errors['password'] = self.error_class(['Passwords not match!'])
                
        return cleaned_data
        