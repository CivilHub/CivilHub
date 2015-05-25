# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from .models import AbuseReport


class BootstrapBaseForm(forms.BaseForm):

    def as_p(self):
        "Returns this form rendered as HTML <p>s."
        return self._html_output(
            normal_row = """<div class="form-group">
                <label class="control-label col-sm-2 custom-tooltip" title="%(help_text)s">%(label)s</label>
                <div class="col-sm-10">%(field)s</div>
            </div>""",
            error_row = '<div class="alert alert-danger">%s</div>',
            row_ender = '</div>',
            help_text_html = '%s',
            errors_on_separate_row = True)


class AbuseReportForm(forms.ModelForm):
    """
    Abuse report form.
    """

    class Meta:
        model = AbuseReport
        fields = ('content_type', 'object_pk', 'comment', 'reason',)
        widgets = {
            'content_type': forms.HiddenInput(),
            'object_pk': forms.HiddenInput(),
            'comment': forms.Textarea(attrs={'class': 'form-control'}),
        }
