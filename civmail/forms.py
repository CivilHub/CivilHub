# -*- coding: utf-8 -*-
import sys
import inspect

from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import translation
from django.utils.translation import ugettext_lazy as _

from locations.models import Location

import messages as mails


class FollowersEmailForm(forms.Form):
    """ This form allows you to write and send messages to location's followers. """
    location_id = forms.IntegerField(widget=forms.HiddenInput())
    subject = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}))

    def clean_location_id(self):
        data = self.cleaned_data['location_id']
        try:
            location = Location.objects.get(pk=data)
        except Location.DoesNotExist:
            raise forms.ValidationError(_(u"Selected location does not exist"))
        return data


class TestSendMailForm(forms.Form):
    """ Test sending emails.
    """
    recipients = forms.ModelMultipleChoiceField(queryset=User.objects.all())
    subject = forms.CharField()
    body = forms.CharField(widget=forms.Textarea)
    context = forms.CharField(widget=forms.Textarea,
                              required=False,
                              help_text=_(u"Additional context in JSON format"))

    def __init__(self, *args, **kwargs):
        super(TestSendMailForm, self).__init__(*args, **kwargs)
        mails = inspect.getmembers(sys.modules['civmail.messages'],
                                   inspect.isclass)
        mails = [(x[0], x[0], ) for x in mails]
        self.fields['message'] = forms.ChoiceField(choices=mails)

    def clean_context(self):
        data = self.cleaned_data['context']
        if not data:
            return {}
        try:
            return json.loads(data)
        except Exception:
            raise forms.ValidationError(u"Context should be in JSON format")

    def is_valid(self):
        valid = super(TestSendMailForm, self).is_valid()
        if not valid:
            return valid
        message = getattr(mails, self.cleaned_data['message'])()
        message_context = self.cleaned_data['context']
        for recipient in self.cleaned_data['recipients']:
            message_context.update({'lang': recipient.profile.lang, })
            message.send(recipient.email, message_context)
        return True


class ContactForm(forms.Form):
    """ Forms for visitors to send messages fo us.
    """
    name = forms.CharField(max_length=128, label=_(u"name"))
    email = forms.EmailField(label=_(u"email"))
    message = forms.CharField(label=_(u"message"), max_length=2048,
        widget=forms.EmailInput(attrs={'maxlength': '2048', }))

    def __init__(self, *args, **kwargs):
        try:
            self.request = kwargs.pop('request')
        except KeyError:
            self.request = None
        super(ContactForm, self).__init__(*args, **kwargs)

    def is_valid(self):
        valid = super(ContactForm, self).is_valid()
        if not valid:
            return valid
        message = mails.ContactEmail()
        message.send(settings.CONTACT_EMAIL_ADDRESS, {
            'sender': self.cleaned_data['name'],
            'email': self.cleaned_data['email'],
            'message': self.cleaned_data['message'], })
        message = mails.ContactResponseEmail()
        email_context = {
            'subject': _("Contact message"),
            'message': self.cleaned_data['message'],
        }
        if self.request is not None:
            email_context.update({
                'lang': translation.get_language_from_request(self.request), })
        message.send(self.cleaned_data['email'], email_context)
        return True
