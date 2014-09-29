# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from places_core.forms import BootstrapBaseForm
from locations.models import Location
from .models import UserGalleryItem, LocationGalleryItem


class BackgroundForm(forms.Form, BootstrapBaseForm):
    """
    Formularz pozwalający użytkownikom wybrać/przyciąć obraz tła dla profilu.
    """
    image = forms.ImageField()
    x = forms.IntegerField(widget=forms.HiddenInput())
    y = forms.IntegerField(widget=forms.HiddenInput())
    x2 = forms.IntegerField(widget=forms.HiddenInput())
    y2 = forms.IntegerField(widget=forms.HiddenInput())


class UserItemForm(forms.ModelForm, BootstrapBaseForm):
    """
    Formularz dodawania/edycji obrazów w galerii użytkownika.
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
    """ Uproszczony formularz umożliwiający edycję metadanych o zdjęciu. """
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
    Formularz dodawania zdjęć do galerii lokalizacji.
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
