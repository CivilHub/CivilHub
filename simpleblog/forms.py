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
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', }),
            'content': forms.Textarea(
                attrs={'class': 'form-control custom-wysiwyg', }),
            'category': forms.Select(attrs={'class': 'form-control', }),
            'tags': forms.TextInput(
                attrs={'class': 'form-control tagsinput', }),
            'content_type': forms.HiddenInput(),
            'object_id': forms.HiddenInput(),
        }
