# -*- coding: utf-8 -*-
from PIL import Image

from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from gallery.image import handle_tmp_image
from locations.models import Location

from .models import Organization


class OrganizationForm(forms.ModelForm):
    """
    Sligthly modified form for organization - edit and create.
    """

    class Meta:
        model = Organization
        exclude = ('slug', 'creator', 'users', 'locations', 'projects',
                   'verified', 'image')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control custom-wysiwyg'}),
            'krs': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'website': forms.TextInput(attrs={'class': 'form-control'}),
            'tags': forms.TextInput(
                attrs={'class': 'form-control custom-tagsinput'}),
        }


class OrganizationLocationForm(forms.Form):
    """
    Allows to choose locations from ID list rather than gets entire queryset.
    """
    locations = forms.CharField(widget=forms.HiddenInput(
        attrs={'class': 'form-control autocomplete-plholder'}))

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
        widget=forms.TextInput(attrs={'class': 'form-control email-input', }))

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


class NGOBackgroundForm(forms.Form):
    """
    Use image crop to change organization's background image.
    """
    image = forms.ImageField(
        label=_(u"Image"),
        widget=forms.FileInput(attrs={'title': _(u"Choose picture")}))
    x = forms.IntegerField(widget=forms.HiddenInput())
    y = forms.IntegerField(widget=forms.HiddenInput())
    x2 = forms.IntegerField(widget=forms.HiddenInput())
    y2 = forms.IntegerField(widget=forms.HiddenInput())
    organization = forms.ModelChoiceField(queryset=Organization.objects.all(),
                                          widget=forms.HiddenInput())

    def is_valid(self):
        valid = super(NGOBackgroundForm, self).is_valid()
        if not valid:
            return valid
        self.save()
        return True

    def save(self, commit=True):
        instance = self.cleaned_data['organization']
        image = Image.open(self.cleaned_data['image'])
        box = (self.cleaned_data['x'], self.cleaned_data['y'],
               self.cleaned_data['x2'], self.cleaned_data['y2'], )
        instance.image = handle_tmp_image(image.crop(box))
        if commit:
            instance.save()
        return instance


class NGOProjectForm(forms.ModelForm):
    """
    Add project to the list of projects where given NGO is a mentor.
    """
    class Meta:
        model = Organization
        fields = ('projects', )
