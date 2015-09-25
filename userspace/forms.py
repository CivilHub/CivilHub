# -*- coding: utf-8 -*-
import json
import urllib
import urllib2

from django import forms
from django.conf import settings
from django.contrib import auth
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from captcha.fields import CaptchaField
from ipware.ip import get_ip

from places_core.forms import BootstrapBaseForm

from .models import UserProfile


class GoogleCaptchaWidget(forms.Widget):
    """ Simplified widget that loads additional scripts from Google.
    """
    template = """<div class="g-recaptcha" data-sitekey="{key}"></div>"""

    def render(self, name, value, attrs=None):
        return self.template.format(key=settings.CAPTCHA_KEY)


class GoogleCaptchaField(forms.Field):
    """ Handle Google Captcha v2 verification.
    """
    widget = GoogleCaptchaWidget


class RegisterForm(UserCreationForm):
    """ Customized user creation form - we check that user email is unique. """
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    password1 = forms.CharField(required=True, widget=forms.PasswordInput())
    password2 = forms.CharField(required=True, widget=forms.PasswordInput())

    # This helps us save form without username - it will be auto-generated
    username = forms.CharField(required=False, widget=forms.HiddenInput())
    captcha = GoogleCaptchaField(label=_(u"captcha"), required=False)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(RegisterForm, self).__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name',
                  'password1', 'password2', 'username')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).count():
            raise forms.ValidationError(_(u'User with this email address already exists.'))
        return email

    def is_valid(self):
        valid = super(RegisterForm, self).is_valid()
        if not valid:
            return valid
        c_response = self.data.get('g-recaptcha-response')
        if c_response is None or not len(c_response):
            msg = _(u"This field is required")
            self._errors['captcha'] = self.error_class([msg])
            return False
        data = urllib.urlencode({
            'secret': settings.CAPTCHA_SECRET,
            'response': c_response,
            'remoteip': get_ip(self.request),})
        google_uri = 'https://www.google.com/recaptcha/api/siteverify'
        response = json.loads(urllib2.urlopen(google_uri, data).read())
        self.cleaned_data['captcha'] = response.get('success')
        if not response.get('success'):
            self._errors['capcha'] = self.error_class([_(u"Invalid captcha")])
            return False
        return True


class LoginForm(forms.Form):
    """ User login form. """
    email = forms.EmailField(required=True, label=_(u"email"))
    password = forms.CharField(
        required = True,
        label = _(u"password"),
        widget = forms.PasswordInput())

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        email = cleaned_data.get('email', None)
        password = cleaned_data.get('password', None)
        user = None
        non_field_errors = []
        if email is None:
            msg = _(u"No email address")
            self.add_error('email', msg)
        if password is None:
            msg = _(u"Password cannot be blank")
            self.add_error('password', msg)
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            msg = _(u"There is no user with this email address")
            non_field_errors.append(msg)
        if user is not None:
            auth_user = auth.authenticate(username=user.username, password=password)
            if auth_user is None:
                msg = _("Wrong password")
                non_field_errors.append(msg)
            elif auth_user is not None and not auth_user.is_active:
                msg = _("Your account is not active yet")
                non_field_errors.append(msg)
            else:
                self.instance = auth_user
        if len(non_field_errors):
            self._errors[forms.forms.NON_FIELD_ERRORS] = self.error_class(non_field_errors)
            if 'email' in cleaned_data: del cleaned_data['email']
            if 'password' in cleaned_data: del cleaned_data['password']
        return cleaned_data


class UserProfileForm(forms.ModelForm, BootstrapBaseForm):
    """ Edit user profile data (excluding picture upload) """
    first_name = forms.CharField(label=_("first name"), max_length=64,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(label=_("Last name"), max_length=64,
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(required=False, label=_("About me"),
        widget=forms.Textarea(attrs={'class': 'form-control'}))
    birth_date = forms.CharField(label=_("Birth date"), required=False,
        widget=forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'birth-date',
                'readonly': 'readonly',
                'placeholder': "dd/mm/yyyy",
            }))

    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'lang', 'description', 'birth_date',
            'gender', 'website', 'gplus_url', 'fb_url', 'twt_url', 'linkedin_url')
        widgets = {
            'lang': forms.Select(attrs={'class': 'form-control'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'website': forms.TextInput(attrs={'class': 'form-control'}),
            'gplus_url': forms.TextInput(attrs={'class': 'form-control'}),
            'fb_url': forms.TextInput(attrs={'class': 'form-control'}),
            'twt_url': forms.TextInput(attrs={'class': 'form-control'}),
            'linkedin_url': forms.TextInput(attrs={'class': 'form-control'}),
        }


class SocialAuthPassetForm(forms.Form):
    """
    Set the user name and pass for users who log in through
    socail auth.
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
        max_length = 64,
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


class PasswordResetForm(forms.Form, BootstrapBaseForm):
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
    A form for users who forgot their password.
    """
    email = forms.EmailField(
        label = '',
        widget = forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _('Enter your email address'), 'autofocus': 'autofocus'})
    )
    captcha = CaptchaField(label=_(u"Retype text from picture"))


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
    A simple form that allows to set the email address of the user that logs
    in through a Twitter account.
    """
    account_email = forms.EmailField(
        label = _("email address"),
        help_text = _("Please provide your email address. Twitter doesn't"),
        widget = forms.EmailInput(attrs={'class': 'form-control'})
    )

    def clean_account_email(self):
        email = self.cleaned_data['account_email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None

        if user is not None:
            raise forms.ValidationError(_(u"Email address already taken"))

        return email
