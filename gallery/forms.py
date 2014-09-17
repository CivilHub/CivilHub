# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from places_core.forms import BootstrapBaseForm
from .models import UserGalleryItem


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