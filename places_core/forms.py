# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from .models import AbuseReport


class AbuseReportForm(forms.ModelForm):
    """
    Abuse report form.
    """
    content_type = forms.ModelChoiceField(
        queryset = ContentType.objects.all(),
        widget = forms.HiddenInput()
    )
    object_pk = forms.IntegerField(
        widget = forms.HiddenInput()
    )
    comment = forms.CharField(
        widget = forms.Textarea(attrs={'class': 'form-control'})
    )

    class Meta:
        model = AbuseReport
        fields = ('content_type', 'object_pk', 'comment',)
