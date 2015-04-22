# -*- coding: utf-8 -*-
from django import forms

from .models import BlogEntry


class BlogEntryForm(forms.ModelForm):
    """
    Use this form in other apps passing proper values for generic foreign key.
    """
    class Meta:
        model = BlogEntry
        exclude = ('slug', 'author', )
