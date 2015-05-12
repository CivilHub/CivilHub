# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

from places_core.forms import BootstrapBaseForm

from .models import Guide, GuideTag


class TagsWidget(forms.TextInput):
    """
    Custom widget to manage tags for guides. It allows us to display model
    choices in text field, like in django-taggit.
    """
    def _format_value(self, value):
        return ", ".join([x[0] for x in GuideTag.objects.filter(pk__in=value).values_list('name')])


class GuideForm(forms.ModelForm, BootstrapBaseForm):
    """ Customized form for guide creation in views tied to location.
    """
    tags = forms.CharField(required=False,
        label= _(u"Tags"),
        widget=TagsWidget(attrs={'class': 'form-control custom-tagsinput', }))

    def __init__(self, *args, **kwargs):
        super(GuideForm, self).__init__(*args, **kwargs)

    def clean_tags(self):
        tags = [x.strip() for x in self.cleaned_data['tags'].split(',') if x]
        tag_objects = []
        for tag in tags:
            tag_objects.append(GuideTag.objects.get_or_create(name=tag)[0])
        return tag_objects

    class Meta:
        model = Guide
        exclude = ('slug', 'owner', 'editors', 'authors', 'location', )
        widgets = {
            'content': forms.Textarea(
                attrs={'class': 'form-control custom-wysiwyg', }),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


class GuideEditorsForm(forms.ModelForm):
    """
    """
    emails = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}), initial="")

    def clean_emails(self):
        emails = [x.strip() for x in self.cleaned_data['emails'].split(',') if x]
        return User.objects.filter(email__in=emails)

    def save(self, commit=True):
        for user in self.cleaned_data['emails']:
            if not user in self.instance.editors.all():
                self.instance.editors.add(user)
        self.instance.save()

    class Meta:
        model = Guide
        fields = ('emails', )
