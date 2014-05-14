# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from taggit.forms import TagField
from locations.models import Location
from .models import Category, Poll


class CategoryForm(forms.ModelForm):
    """
    Custom form to add Bootstrap classes etc.
    """
    name = forms.CharField(
        required = True,
        max_length = 128,
        widget = forms.TextInput(attrs={'class':'form-control'})
    )
    description = forms.CharField(
        required = True,
        max_length = 2048,
        widget = forms.Textarea(attrs={'class':'form-control'})
    )

    class Meta:
        model = Category
        fields = '__all__'


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
    category = forms.ModelChoiceField(
        required = False,
        queryset = Category.objects.all(),
        widget = forms.Select(attrs={'class':'form-control'})
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
        fields = ('title', 'description', 'category', 'location', 'tags')
    