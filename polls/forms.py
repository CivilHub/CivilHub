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
        widget = forms.Textarea(attrs={'class':'form-control'})
    )
    categories = forms.ModelMultipleChoiceField(
        queryset = Category.objects.all(),
        widget = forms.SelectMultiple(attrs={'class':'form-control'})
    )
    location = forms.ModelChoiceField(
        queryset = Location.objects.all(),
        widget = forms.HiddenInput()
    )
    tags = TagField()
    
    class Meta:
        model = Poll
        fields = ('title', 'description', 'categories', 'location', 'tags')
    