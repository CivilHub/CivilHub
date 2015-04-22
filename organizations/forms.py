# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from taggit.forms import TagField

from locations.models import Location

from .models import Organization


class OrganizationForm(forms.ModelForm):
    """
    Sligthly modified form for organization - edit and create.
    """

    class Meta:
        model = Organization
        exclude = ('slug', 'creator', 'users', 'locations', 'projects',
                   'verified', 'image' )
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control custom-wysiwyg'}),
            'krs': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'website': forms.TextInput(attrs={'class': 'form-control'}),
        }


class OrganizationLocationForm(forms.Form):
    """
    Allows to choose locations from ID list rather than gets entire queryset.
    """
    locations = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control autocomplete-plholder'}))

    def clean_locations(self):
        id_list = [int(x) for x in self.cleaned_data['locations'].split(',')]
        return Location.objects.filter(pk__in=id_list)


class NGOInviteForm(forms.Form):
    """
    Form that allow creators and superusers to invite others to join their
    organizations. By filling form we create Invitation objects.
    """
    organization = forms.ModelChoiceField(queryset=Organization.objects.all(),
                                          widget=forms.HiddenInput())
    emails = forms.CharField(
        label=_(u"Emails"),
        help_text=_(u"Enter email addresses separated with comma"),
        widget=forms.TextInput(attrs={'class': 'email-input', }))

    def clean_emails(self):
        emails = [x.strip() for x in self.cleaned_data['emails'].split(',')]
        invalid_emails = []
        self.users = []
        for email in emails:
            try:
                self.users.append(User.objects.get(email=email))
            except User.DoesNotExist:
                invalid_emails.append(email)
        if len(invalid_emails):
            raise forms.ValidationError(
                _(u"Invalid user emails: ") + ", ".join(invalid_emails))
        return emails
