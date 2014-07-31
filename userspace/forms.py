# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import UserProfile


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
    first_name = forms.CharField(
        label = _("First name"),
        max_length = 30,
        widget = forms.TextInput(attrs={'class': 'form-control', 'id': 'first-name',})
    )
    last_name = forms.CharField(
        label = _("Last name"),
        max_length = 30,
        widget = forms.TextInput(attrs={'class': 'form-control', 'id': 'last-name',})
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


class SocialAuthPassetForm(forms.Form):
    """
    Ustawienie nazwy użytkownika i hasła dla użytkowników
    logujących się przez social auth.
    """
    username = forms.CharField(
        label = _('Username'),
        max_length = 32,
        widget = forms.TextInput(attrs={'class': 'form-control', 'id': 'username', 'placeholder': _('Select username')})
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
        super(SocialAuthPassetForm, self).__init__(*args, **kwargs)

    def clean(self):
        try:
            chk_user = User.objects.get(username=self.cleaned_data.get('username'))
            raise ValidationError(_('Username already taken. Pick another one!'))
        except User.DoesNotExist:
            pass
        return super(SocialAuthPassetForm, self).clean()


class LoginForm(forms.Form):
    """
    Login registered user
    """
    email = forms.CharField(
        label = _('Email'),
        max_length = 32,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'id': 'username', 'placeholder': _('Select username')})
    )
    password = forms.CharField(
        label = _('Password'),
        max_length = 64,
        widget = forms.PasswordInput(attrs={'class': "form-control", 'id': 'password'})
    )
    remember_me = forms.BooleanField(
        label = _("Remember me"),
        required = False,
        widget = forms.CheckboxInput(attrs={'checked': 'checked'})
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
    description = forms.CharField(
        label = _("About me"),
        max_length = 10248,
        required = False,
        widget = forms.Textarea(attrs={'class': 'form-control'})
    )
    birth_date = forms.CharField(
        label = _("Birth date"),
        max_length = 10,
        required = False,
        widget = forms.TextInput(attrs={'class':'form-control','id':'birth-date',})
    )

    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'description', 'birth_date')


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


class PasswordRemindForm(forms.Form):
    """
    Formularz dla użytkowników, którzy zapomnieli hasła.
    """
    email = forms.EmailField(
        label = _("Email address"),
        widget = forms.EmailInput(attrs={'class': 'form-control'})
    )


class AvatarUploadForm(forms.Form):
    """
    Upload user avatar
    """
    avatar = forms.FileField(
        label = "",
        help_text = "",
        widget = forms.FileInput(attrs={'title':_('Change')})
    )


class TwitterEmailForm(forms.Form):
    """
    Prosty formularz do ustawienia adresu email użytkownika logującego się
    przy pomocy konta na Twitterze.
    """
    account_email = forms.EmailField(
        label = _("email address"),
        help_text = _("Please provide your email address. Twitter doesn't"),
        widget = forms.EmailInput(attrs={'class': 'form-control'})
    )