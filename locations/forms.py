# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext as _
from taggit.forms import TagField
from ideas.models import Idea
from locations.models import Location

class LocationForm(forms.ModelForm):
    """
    Edit/update/create location form
    """
    class Meta:
        model = Location


class IdeaLocationForm(forms.ModelForm):
    """
    Custom form for place - autocomplete value of location field.
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
