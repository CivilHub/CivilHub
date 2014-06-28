# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from locations.models import Location
from taggit.forms import TagField
from .models import Category, Entry, Discussion


class DiscussionForm(forms.ModelForm):
    """
    Custom form for Discussion - autocomplete value of location field.
    """
    question = forms.CharField(
        widget = forms.TextInput(attrs={'class': 'form-control'})
    )
    intro = forms.CharField(
        max_length = 10248,
        widget = forms.Textarea(attrs={'class': 'form-control'})
    )
    category = forms.ModelChoiceField(
        queryset = Category.objects.all(),
        widget = forms.Select(attrs={'class': 'form-control'})
    )
    location = forms.ModelChoiceField(
        required = True,
        queryset = Location.objects.all(),
        widget = forms.Select(attrs={'class': 'form-control'})
    )
    status = forms.BooleanField(
        required = False,
        label = _('Status'),
    )
    tags = TagField(required=False)

    class Meta:
        model = Discussion
        fields = ('question', 'intro', 'category', 'location', 'status', 'tags')


class ReplyForm(forms.ModelForm):
    """
    Reply to discussion topic.
    """
    content = forms.CharField(
        required = True,
        max_length = 2048,
        widget = forms.Textarea(attrs={'class': 'form-control'}),
    )
    discussion = forms.ModelChoiceField(
        required = True,
        queryset = Discussion.objects.all(),
        widget = forms.HiddenInput()
    )

    class Meta:
        model = Entry
        fields = ('content', 'discussion',)
