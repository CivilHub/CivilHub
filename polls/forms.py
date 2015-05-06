# -*- coding: utf-8 -*-
import json

from django import forms
from django.utils.translation import ugettext_lazy as _

from taggit.forms import TagField

from locations.models import Location
from places_core.forms import BootstrapBaseForm

from .models import Poll, SimplePollAnswerSet, SimplePollQuestion


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


class SimplePollForm(forms.Form):
    """ Form allowing users to participate in simple polls.
    """
    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance')
        self.user = kwargs.pop('user')
        super(SimplePollForm, self).__init__(*args, **kwargs)
        for question in self.instance.simplepollquestion_set.all():
            self.create_field(question)

    def create_field(self, question):
        if question.question_type == 1 or question.question_type == 2:
            self.create_choice_field(question)
        else:
            self.fields["question_%d" % question.pk] = forms.CharField(
                label=question.text,
                widget=forms.Textarea(attrs={'class': 'form-control'}))

    def create_choice_field(self, question):
        if question.question_type == 1:
            self.fields["question_%d" % question.pk] = forms.ModelChoiceField(
                label=question.text,
                widget=forms.RadioSelect,
                empty_label=None,
                queryset=question.simplepollanswer_set.all()
            )
        else:
            self.fields["question_%d" % question.pk] = forms.ModelMultipleChoiceField(
                label=question.text,
                widget=forms.CheckboxSelectMultiple,
                queryset=question.simplepollanswer_set.all()
            )

    def is_valid(self):
        valid = super(SimplePollForm, self).is_valid()
        if not valid:
            return valid
        for field, value in self.cleaned_data.iteritems():
            field_type = self.fields[field].__class__.__name__
            if field_type == 'ModelChoiceField':
                answer = ",".join([str(value.pk), ])
            elif field_type == 'ModelMultipleChoiceField':
                answer = ",".join([str(x.pk) for x in value])
            else:
                answer = value
            question = SimplePollQuestion.objects.get(pk=int(field.split('_')[-1]))
            answer_set = SimplePollAnswerSet.objects.create(
                user=self.user,
                poll=self.instance,
                question=question,
                answer=answer)
        return True
