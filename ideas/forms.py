# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from taggit.forms import TagField
from ideas.models import Idea, Category
from locations.models import Location


class CategoryForm(forms.ModelForm):
    """
    Create/edit categories for ideas.
    """
    name = forms.CharField(
        max_length = 64,
        widget = forms.TextInput(attrs={
            'class': 'form-control',
            'autofocus': 'autofocus'
        })
    )
    description = forms.CharField(
        max_length = 1024,
        widget = forms.Textarea(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Category
        fields = ('name', 'description',)


class IdeaForm(forms.ModelForm):
    """
    Edit/update/create idea form
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
    category = forms.ModelChoiceField(
        required = False,
        queryset = Category.objects.all(),
        widget = forms.Select(attrs={'class': 'form-control'})
    )
    location = forms.ModelChoiceField(
        required = True,
        queryset = Location.objects.all(),
        widget = forms.Select(attrs={'class': 'form-control'})
    )
    tags = TagField()

    class Meta:
        model = Idea
        fields = ('name', 'description', 'location', 'tags')
