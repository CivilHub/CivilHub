# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from taggit.forms import TagField
from ideas.models import Idea
from locations.models import Location

class LocationForm(forms.ModelForm):
    """
    Edit/update/create location form
    """
    name = forms.CharField(
        required = True,
        max_length = 64,
        label = _('Name'),
        widget = forms.TextInput(attrs={'class': 'form-control'})
    )
    description = forms.CharField(
        required = False,
        max_length = 1024,
        label = _('Description'),
        widget = forms.Textarea(attrs={'class': 'form-control'})
    )
    latitude = forms.FloatField(
        required = True,
        label = _('Latitude'),
        min_value = 0,
        max_value = 360,
        widget = forms.NumberInput(attrs={'class': 'form-control'})
    )
    longitude = forms.FloatField(
        required = True,
        label = _('Longitude'),
        min_value = 0,
        max_value = 360,
        widget = forms.NumberInput(attrs={'class': 'form-control'})
    )
    image = forms.ImageField(
        required = False,
        label = _('Image')
    )

    class Meta:
        model = Location
        fields = ('name', 'description', 'latitude', 'longitude', 'image',)


class IdeaLocationForm(forms.ModelForm):
    """
    Custom form for Idea - autocomplete value of location field.
    """
    name = forms.CharField(
        required = True,
        max_length = 64,
        widget = forms.TextInput(attrs={'class': 'form-control'})
    )
    description = forms.CharField(
        required = False,
        max_length = 2048,
        widget = forms.Textarea(attrs={'class': 'form-control'})
    )
    location = forms.ModelChoiceField(
        required = True,
        queryset = Location.objects.all(),
        widget = forms.HiddenInput()
    )
    tags = TagField()

    class Meta:
        model = Idea
        fields = ('name', 'description', 'location', 'tags')
