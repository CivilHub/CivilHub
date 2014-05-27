# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
import models


class MapPointerForm(forms.ModelForm):
    """
    Custom pointer form for testing purposes. This form
    is rendered as static page instead of AJAXy form.
    """
    content_type = forms.ModelChoiceField(
        label = _("Content type"),
        queryset = ContentType.objects.all(),
        widget = forms.Select(attrs={'class': 'form-control'})
    )
    object_pk = forms.IntegerField(
        label = _("Object id"),
        widget = forms.NumberInput(attrs={'class': 'form-control'})
    )
    latitude = forms.FloatField(widget=forms.HiddenInput())
    longitude = forms.FloatField(widget=forms.HiddenInput())

    class Meta:
        model = models.MapPointer
        fields = ('content_type', 'object_pk', 'latitude', 'longitude',)
