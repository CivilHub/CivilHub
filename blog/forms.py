# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _

from taggit.forms import TagField

from places_core.forms import BootstrapBaseForm

from .models import Category, News


class NewsForm(forms.ModelForm, BootstrapBaseForm):
    """ Edit/update/create blog entry. """
    title = forms.CharField(
        label = _(u"Title"),
        required = True,
        widget = forms.TextInput(attrs={'class': 'form-control'})
    )
    content = forms.CharField(
        label = _(u"Content"),
        required = True, 
        widget = forms.Textarea(attrs={'class': 'form-control'})
    )
    tags = TagField(label=_(u"Tags"), required=False)

    class Meta:
        model = News
        exclude = ('edited', 'slug', 'creator',)
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.HiddenInput(),
        }
