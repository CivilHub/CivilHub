# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User

class RegisterForm(forms.Form):
    """
    Register new user
    """
    username = forms.CharField(
        label = _('Username'),
        max_length = 32,
        widget = forms.TextInput(attrs={'class': 'form-control', 'id': 'username', 'placeholder': _('Select username')})
    )
    email = forms.CharField(
        label = _("Email"),
        max_length = 128,
        widget = forms.EmailInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label = _('Password'),
        max_length = 64,
        widget = forms.PasswordInput(attrs={'class': "form-control", 'id': 'password'})
    )
    passchk = forms.CharField(
        label = _("Repeat password"),
        max_length = 32,
        widget = forms.PasswordInput(attrs={'class': "form-control", 'id': 'passchk'})
    )
    
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(RegisterForm, self).__init__(*args, **kwargs)
        
    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')
        email    = cleaned_data.get('email')
        passchk  = cleaned_data.get('passchk')
        if User.objects.filter(username=username).exists():
            self._errors['username'] = self.error_class([_('Username already taken. Pick another one!')])
            del cleaned_data['username']
        if User.objects.filter(email=email).exists():
            self._errors['email'] = self.error_class([_('Email already taken. Pick another one!')])
            del cleaned_data['email']
        if (password != passchk):
            self._errors['password'] = self.error_class([_('Passwords not match!')])
                
        return cleaned_data
    
class LoginForm(forms.Form):
    """
    Login registered user
    """
    username = forms.CharField(
        label = _('Username'),
        max_length = 32,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'username', 'placeholder': _('Select username')})
    )
    password = forms.CharField(
        label = _('Password'),
        max_length = 64,
        widget = forms.PasswordInput(attrs={'class': "form-control", 'id': 'password'})
    )
    
class UserProfileForm(forms.Form):
    """
    Edit user profile data (excluding picture upload)
    """ 
    first_name = forms.CharField(
        label = _("First name"),
        max_length = 64,
        required = False,
        widget = forms.TextInput(attrs={'class':'form-control','id':'first-name','placeholder':_('First name')})                         
    )
    last_name = forms.CharField(
        label = _("Last name"),
        max_length = 64,
        required = False,
        widget = forms.TextInput(attrs={'class':'form-control','id':'last-name','placeholder':_('Last name')})                         
    )
    email = forms.EmailField(
        label = _("Email"),
        max_length = 64,
        required = False,
        widget = forms.EmailInput(attrs={'class':'form-control','id':'email','placeholder':_('Email address')})                         
    )
    birth_date = forms.CharField(
        label = _("Birth date"),
        max_length = 10,
        required = False,
        widget = forms.TextInput(attrs={'class':'form-control','id':'birth-date',})
    )
    
class PasswordResetForm(forms.Form):
    """
    Allow users to change their passwords
    """
    current = forms.CharField(
        label = _("Current password"),
        max_length = 64,
        required = True,
        widget = forms.PasswordInput(attrs={'class':'form-control','id':'current'})
    )
    password = forms.CharField(
        label = _("New password"),
        max_length = 64,
        required = True,
        widget = forms.PasswordInput(attrs={'class':'form-control','id':'password'})
    )
    passchk = forms.CharField(
        label = _("Retype password"),
        max_length = 64,
        required = True,
        widget = forms.PasswordInput(attrs={'class':'form-control','id':'passchk'})
    )
    def clean(self):
        cleaned_data = super(PasswordResetForm, self).clean()
        password = cleaned_data.get('password')
        passchk  = cleaned_data.get('passchk')
        if (password != passchk):
            self._errors['password'] = self.error_class([_('Passwords not match!')])
            
        return cleaned_data
    
class AvatarUploadForm(forms.Form):
    """
    Upload user avatar
    """
    avatar = forms.FileField(
        label="",
        help_text="",
        widget = forms.FileInput(attrs={'title':_('Change')})
    )
