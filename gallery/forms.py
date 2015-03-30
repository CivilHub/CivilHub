# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from places_core.forms import BootstrapBaseForm
from locations.models import Location
from .models import UserGalleryItem, LocationGalleryItem


class BackgroundForm(forms.Form, BootstrapBaseForm):
    """
    Form allows users to select / crop the image background for the profile.
    """
    image = forms.ImageField(
        label = _("Image"),
        widget = forms.FileInput(attrs={'title':_("Choose picture")})
    )
    x = forms.IntegerField(widget=forms.HiddenInput())
    y = forms.IntegerField(widget=forms.HiddenInput())
    x2 = forms.IntegerField(widget=forms.HiddenInput())
    y2 = forms.IntegerField(widget=forms.HiddenInput())


class UserItemForm(forms.ModelForm, BootstrapBaseForm):
    """
    Form to add / edit images in user gallery's.
    """
    image = forms.ImageField(
        label=u'',
        required = True
    )
    name = forms.CharField(
        required = False,
        label = _("Name"),
        widget = forms.TextInput(attrs={'class':'form-control'})
    )
    description = forms.CharField(
        required = False,
        label = _("Description"),
        widget = forms.Textarea(attrs={'class':'form-control'})
    )

    class Meta:
        model = UserGalleryItem
        fields = ('image', 'name', 'description',)


class SimpleItemForm(forms.ModelForm, BootstrapBaseForm):
    """ Simplified form to edit the metadata of the photo. """
    name = forms.CharField(
        required = False,
        label = _("Name"),
        widget = forms.TextInput(attrs={'class':'form-control'})
    )
    description = forms.CharField(
        required = False,
        label = _("Description"),
        widget = forms.Textarea(attrs={'class':'form-control'})
    )

    class Meta:
        model = UserGalleryItem
        fields = ('name', 'description',)


class LocationItemForm(forms.ModelForm, BootstrapBaseForm):
    """
    Form to add photos to the gallery location.
    """
    image = forms.ImageField(
        label=u'',
        required = True
    )
    name = forms.CharField(
        required = False,
        label = _("Name"),
        widget = forms.TextInput(attrs={'class':'form-control'})
    )
    description = forms.CharField(
        required = False,
        label = _("Description"),
        widget = forms.Textarea(attrs={'class':'form-control'})
    )
    location= forms.ModelChoiceField(
        required = True,
        queryset = Location.objects.all(),
        widget = forms.HiddenInput()
    )

    class Meta:
        model = LocationGalleryItem
        fields = ('image', 'name', 'description', 'location',)
