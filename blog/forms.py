# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _

from taggit.forms import TagField

from places_core.forms import BootstrapBaseForm

from .models import Category, News


class NewsForm(forms.ModelForm, BootstrapBaseForm):
    """ Edit/update/create blog entry. """
    tags = TagField(required=False, label= _(u"Tags"))

    class Meta:
        model = News
        exclude = ('edited', 'slug', 'creator',)
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control custom-wysiwyg'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.HiddenInput(),
            'image': forms.ClearableFileInput(attrs={'class': 'civ-img-input', }),
        }
