# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _
from taggit.forms import TagField
from locations.models import Location
from .models import Category, Poll


class CategoryForm(forms.ModelForm):
    """
    Custom form to add Bootstrap classes etc.
    """
    name = forms.CharField(
        required = True,
        max_length = 128,
        widget = forms.TextInput(attrs={'class':'form-control'})
    )
    description = forms.CharField(
        required = True,
        max_length = 2048,
        widget = forms.Textarea(attrs={'class':'form-control'})
    )

    class Meta:
        model = Category
        fields = '__all__'


class PollForm(forms.ModelForm):
    """
    Custom poll form - we will bind it with scripts on client-side.
    """
    title = forms.CharField(
        widget = forms.TextInput(attrs={'class':'form-control'})
    )
    description = forms.CharField(
        required = False,
        widget = forms.Textarea(attrs={'class':'form-control'})
    )
    category = forms.ModelChoiceField(
        required = False,
        queryset = Category.objects.all(),
        widget = forms.Select(attrs={'class':'form-control'})
    )
    location = forms.ModelChoiceField(
        queryset = Location.objects.all(),
        widget = forms.HiddenInput()
    )
    tags = TagField(
        required = False
    )
    
    class Meta:
        model = Poll
        fields = ('title', 'description', 'category', 'location', 'tags')


class PollEntryAnswerForm(forms.Form):
    """
    Print form for single poll's question and let user participate!
    """
    def __init__(self, qset):
        super(PollEntryAnswerForm, self).__init__()
        for q in qset:
            if q.multiple:
                field_type = forms.MultipleChoiceField
                widget_type = forms.CheckboxSelectMultiple
            else:
                field_type = forms.ChoiceField
                widget_type = forms.RadioSelect
            a_keys = []
            a_labels = []
            for a in q.answer_set.all():
                a_labels.append((a.pk, a.answer))
            self.fields['question_' + str(q.pk)] = field_type(
                label = q.question,
                choices = a_labels,
                widget = widget_type()
            )
