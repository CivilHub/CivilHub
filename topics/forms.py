# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from .models import Entry, Discussion


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
