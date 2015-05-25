# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from locations.models import Location
from taggit.forms import TagField
from places_core.forms import BootstrapBaseForm
from .models import Category, Entry, Discussion


class DiscussionForm(forms.ModelForm, BootstrapBaseForm):
    """
    Custom form for Discussion - autocomplete value of location field.
    """
    question = forms.CharField(
        label = _(u'Question'),
        widget = forms.TextInput(attrs={'class': 'form-control'})
    )
    intro = forms.CharField(
        label = _(u'Intro'),
        max_length = 10248,
        widget = forms.Textarea(attrs={'class': 'form-control'})
    )
    category = forms.ModelChoiceField(
        label = _(u'Category'),
        queryset = Category.objects.all(),
        widget = forms.Select(attrs={'class': 'form-control'})
    )
    status = forms.BooleanField(
        required = False,
        label = _(u'Status'),
    )
    tags = TagField(label=_(u"Tags"), required=False)

    class Meta:
        model = Discussion
        fields = ('question', 'intro', 'category', 'status', 'tags', 'image',)


class ReplyForm(forms.ModelForm):
    """
    Reply to discussion topic.
    """
    content = forms.CharField(
        label = _(u'Content'),
        required = False,
        max_length = 2048,
        widget = forms.Textarea(attrs={'class': 'form-control'}),
    )
    discussion = forms.ModelChoiceField(
        required = False,
        queryset = Discussion.objects.all(),
        widget = forms.HiddenInput()
    )

    class Meta:
        model = Entry
        fields = ('content', 'discussion',)


class ConfirmDeleteForm(forms.Form):
    """
    Delete discussion.
    """
    confirm = forms.BooleanField(
        widget = forms.HiddenInput()
    )

    class Meta:
        fields = ('confirm',)
