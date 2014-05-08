# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from taggit.forms import TagField
from blog.models import News
from locations.models import Location


class NewsForm(forms.ModelForm):
    """
    Edit/update/create idea form
    """
    title = forms.CharField(
        required = True,
        max_length = 64,
        label = _('Title'),
        widget = forms.TextInput(attrs={'class': 'form-control'})
    )
    content = forms.CharField(
        required = False,
        max_length = 10248,
        label = _('Content'),
        widget = forms.Textarea(attrs={'class': 'form-control'})
    )
    categories = forms.ModelMultipleChoiceField(
        required = False,
        queryset = Location.objects.all(),
        label = _('Categories'),
        widget = forms.SelectMultiple(attrs={'class': 'form-control'})
    )
    tags = TagField()

    class Meta:
        model = News
        fields = ('title', 'content', 'categories', 'tags')
