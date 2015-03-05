# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from taggit.forms import TagField
from locations.models import Location
from places_core.forms import BootstrapBaseForm
from .models import Poll


class PollForm(forms.ModelForm, BootstrapBaseForm):
    """
    Custom poll form - we will bind it with scripts on client-side.
    """
    title = forms.CharField(
        label = _(u"Title"),
        required = True,
        widget = forms.TextInput(attrs={'class':'form-control'})
    )
    question = forms.CharField(
        label = _(u"Question"),
        widget = forms.Textarea(attrs={'class':'form-control'})
    )
    location = forms.ModelChoiceField(
        queryset = Location.objects.all(),
        widget = forms.HiddenInput()
    )
    multiple = forms.BooleanField(
        label = _(u"Multiple"),
        required = False
    )
    tags = TagField(label=_(u"Tags"), required = False)
    
    class Meta:
        model = Poll
        fields = ('title', 'question', 'location', 'multiple', 'tags', 'image')


class PollEntryAnswerForm(forms.Form):
    """
    Print form for single poll's question and let user participate!
    aset param means answer set for given poll, this class will create
    appropriate view based on answer set and poll type (multiple or not).
    """
    def __init__(self, poll):
        super(PollEntryAnswerForm, self).__init__()
        if poll.multiple:
            widget_type = forms.CheckboxInput
            for a in poll.answer_set.all():
            #answers.append((a.pk, a.answer))
                self.fields['answer_' + str(a.pk)] = forms.ChoiceField(
                    label = a.answer,
                    widget = widget_type()
                )
        else:
            widget_type = forms.RadioSelect
            answers = []
            for a in poll.answer_set.all():
                answers.append((a.pk, a.answer))
                self.fields['answers'] = forms.ChoiceField(
                    label = _('Select answer'),
                    choices = answers,
                    widget = widget_type()
                )
        self.fields['poll'] = forms.ModelChoiceField(
            queryset = Poll.objects.all(),
            initial = poll,
            widget = forms.HiddenInput()
        )
