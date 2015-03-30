# -*- coding: utf-8 -*-
from django import forms
from django.forms.util import ErrorList
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

from taggit.forms import TagField
from haystack.forms import SearchForm

from maps.models import MapPointer
from ideas.models import Idea
from ideas.models import Category as IdeaCategory
from blog.models import News
from blog.models import Category as BlogCategory
from topics.models import Discussion, Entry
from topics.models import Category as ForumCategory
from places_core.forms import BootstrapBaseForm

from .models import Location, Country


class LocationForm(forms.ModelForm, BootstrapBaseForm):
    """
    Edit/update/create location form
    """
    name = forms.CharField(
        required = True,
        max_length = 64,
        label = _('Name'),
        widget = forms.TextInput(attrs={'class': 'form-control'})
    )
    country_code = forms.ModelChoiceField(
        required = True,
        label = _("Country code"),
        queryset = Country.objects.all(),
        widget = forms.Select(attrs={'class':'form-control'})
    )
    description = forms.CharField(
        required = False,
        max_length = 10000,
        label = _('Description'),
        widget = forms.Textarea(attrs={'class': 'form-control'})
    )
    parent = forms.IntegerField(
        label = _('Parent'),
        required = False,
        help_text = _("Choose parent location for your place. You can see which place is currently selected in grey box above."),
        widget = forms.TextInput()
    )
    latitude = forms.FloatField(
        required = False,
        label = _('Latitude'),
        widget = forms.TextInput(attrs={'class': 'form-control'})
    )
    longitude = forms.FloatField(
        required = False,
        label = _('Longitude'),
        widget = forms.TextInput(attrs={'class': 'form-control'})
    )
    population = forms.IntegerField(
        required = False,
        label = _("Population"),
        widget = forms.NumberInput(attrs={'class': 'form-control'})
    )
    image = forms.ImageField(
        required = False,
        label = _('Image')
    )
    
    def clean(self):
        cparent = self.cleaned_data.get('parent', None)
        if cparent is None: return self.cleaned_data
        try:
            parent = Location.objects.get(pk=cparent)
            self.cleaned_data['parent'] = parent
        except Location.DoesNotExist:
            msg = _("Selected location does not exist")
            self._errors['parent'] = ErrorList([msg])
            del self.cleaned_data['parent']
        
        return self.cleaned_data

    def save(self, force_insert=False, force_update=False, commit=True):
        location = super(LocationForm, self).save()
        lat = self.cleaned_data.get('latitude')
        lng = self.cleaned_data.get('longitude')
        if lat and lng:
            marker = MapPointer.objects.create(
                content_type=ContentType.objects.get_for_model(location),
                object_pk=location.pk,
                latitude=lat, longitude=lng
            )
        return location

    class Meta:
        model = Location
        fields = ('name', 'description', 'country_code', 'parent',
                  'population', 'latitude', 'longitude',)


class IdeaLocationForm(forms.ModelForm, BootstrapBaseForm):
    """
    Custom form for Idea - autocomplete value of location field.
    """
    name = forms.CharField(
        label = _("Name"),
        required = True,
        max_length = 64,
        widget = forms.TextInput(attrs={'class': 'form-control'})
    )
    description = forms.CharField(
        label = _("Description"),
        required = False,
        max_length = 20480,
        widget = forms.Textarea(attrs={'class': 'form-control'})
    )
    category = forms.ModelChoiceField(
        label = _("Category"),
        required = False,
        queryset = IdeaCategory.objects.all(),
        widget = forms.Select(attrs={'class': 'form-control'})
    )
    location = forms.ModelChoiceField(
        required = True,
        queryset = Location.objects.all(),
        widget = forms.HiddenInput()
    )
    tags = TagField(label=_("Tags"), required=False)

    class Meta:
        model = Idea
        fields = ('name', 'description', 'location', 'tags', 'category', 'image')


class DiscussionLocationForm(forms.ModelForm, BootstrapBaseForm):
    """
    Custom form for Discussion - autocomplete value of location field.
    """
    question = forms.CharField(
        label = _("Question"),
        widget = forms.TextInput(attrs={'class': 'form-control'})
    )
    intro = forms.CharField(
        label = _("Intro"),
        max_length = 10248,
        widget = forms.Textarea(attrs={'class': 'form-control'})
    )
    category = forms.ModelChoiceField(
        label = _("Category"),
        queryset = ForumCategory.objects.all(),
        widget = forms.Select(attrs={'class': 'form-control'})
    )
    location = forms.ModelChoiceField(
        required = True,
        queryset = Location.objects.all(),
        widget = forms.HiddenInput()
    )
    tags = TagField(label=_("Tags"), required=False)

    class Meta:
        model = Discussion
        fields = ('question', 'intro', 'category', 'location', 'tags', 'image')


class SearchDiscussionForm(SearchForm):
    """
    A form for searching for discussion in the current location.
    """
    q = forms.CharField(
        label = "",
        widget = forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        fields = ('q',)

    def search(self):
        sqs = super(SearchDiscussionForm, self).search()

        if not self.is_valid():
            return self.no_query_found()

        if self.cleaned_data['location']:
            sqs = sqs.filter(location=location)

        return sqs


class InviteUsersForm(forms.Form):
    """
    A form for sending invites to other users.
    """
    location = forms.ModelChoiceField(
        queryset = Location.objects.all(),
        widget   = forms.HiddenInput()
    )
    user = forms.ModelMultipleChoiceField(
        label    = _("Select users"),
        queryset = User.objects.all(),
        widget   = forms.SelectMultiple(attrs={'class': 'form-control'})
    )
