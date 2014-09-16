# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from .models import AbuseReport


class BootstrapBaseForm(forms.BaseForm):

    def as_p(self):
        "Returns this form rendered as HTML <p>s."
        return self._html_output(
            normal_row = '<div class="form-group"><label class="control-label col-sm-2">%(label)s</label><div class="col-sm-10">%(field)s%(help_text)s</div></div>',
            error_row = '<div class="alert alert-danger">%s</div>',
            row_ender = '</div>',
            help_text_html = '<span class="help-block">%s</span>',
            errors_on_separate_row = True)


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
