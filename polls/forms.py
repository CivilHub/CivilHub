# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from taggit.forms import TagField
from locations.models import Location
from .models import Poll


class PollForm(forms.ModelForm):
    """
    Custom poll form - we will bind it with scripts on client-side.
    """
    title = forms.CharField(
        widget = forms.TextInput(attrs={'class':'form-control'})
    )
    question = forms.CharField(
        widget = forms.Textarea(attrs={'class':'form-control'})
    )
    location = forms.ModelChoiceField(
        queryset = Location.objects.all(),
        widget = forms.HiddenInput()
    )
    multiple = forms.BooleanField(
        required = False
    )
    tags = TagField(
        required = False
    )
    
    class Meta:
        model = Poll
        fields = ('title', 'question', 'location', 'multiple', 'tags',)


class PollEntryAnswerForm(forms.Form):
    """
    Print form for single poll's question and let user participate!
    aset param means answer set for given poll, this class will create
    appropriate view based on answer set and poll type (multiple or not).
    """
    def __init__(self, poll):
        super(PollEntryAnswerForm, self).__init__()
        if poll.multiple:
            field_type = forms.MultipleChoiceField
            widget_type = forms.CheckboxSelectMultiple
        else:
            field_type = forms.ChoiceField
            widget_type = forms.RadioSelect
        answers = []
        for a in poll.answer_set.all():
            answers.append((a.pk, a.answer))
        self.fields[poll.question] = field_type(
            label = _('Select answer'),
            choices = answers,
            widget = widget_type()
        )
