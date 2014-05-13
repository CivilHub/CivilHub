# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from taggit.forms import TagField
from locations.models import Location
from .models import Category, Poll


class PollForm(forms.ModelForm):
    """
    Custom poll form - we will bind it with scripts on client-side.
    """
    title = forms.CharField(
        widget = forms.TextInput(attrs={'class':'form-control'})
    )
    description = forms.CharField(
        required = False,
        widget = forms.Textarea(attrs={'class':'form-control'})
    )
    categories = forms.ModelMultipleChoiceField(
        required = False,
        queryset = Category.objects.all(),
        widget = forms.SelectMultiple(attrs={'class':'form-control'})
    )
    location = forms.ModelChoiceField(
        queryset = Location.objects.all(),
        widget = forms.HiddenInput()
    )
    tags = TagField(
        required = False
    )
    
    class Meta:
        model = Poll
        fields = ('title', 'description', 'categories', 'location', 'tags')
    