# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.contrib.contenttypes.models import ContentType

from .models import Voting


class VotingForm(forms.ModelForm):
    """ This is semi-automated form for ``Voting`` model.

    This form takes few additional arguments for initializer, namely:
        ::request - Django ``Request`` instance taken from view.
        ::content_object - Any model instance that may be related by
    Django's GenericForeignKey.
    """
    class Meta:
        model = Voting
        exclude = ('author', 'content_type', 'object_id',)
        widgets = {
            'start_date': forms.TextInput(attrs={
                'readonly': 'readonly',
                'class': 'form-control custom-datepicker'}),
            'finish_date': forms.TextInput(attrs={
                'readonly': 'readonly',
                'class': 'form-control custom-datepicker'}),}

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        try:
            self.content_object = kwargs.pop('content_object')
        except KeyError:
            self.content_object = None
        super(VotingForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        if self.content_object is None:
            ct = None
            pk = None
        else:
            ct = ContentType.objects.get_for_model(self.content_object)
            pk = self.content_object.pk
        self.instance.author = self.request.user
        self.instance.content_type = ct
        self.instance.object_id = pk
        return super(VotingForm, self).save(commit=commit)

