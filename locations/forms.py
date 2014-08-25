# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from taggit.forms import TagField
from ideas.models import Idea
from ideas.models import Category as IdeaCategory
from blog.models import News
from blog.models import Category as BlogCategory
from locations.models import Location, get_country_codes
from topics.models import Discussion, Entry
from topics.models import Category as ForumCategory
from haystack.forms import SearchForm
from geobase.models import Country


def get_country_names():
    """ Funkcja zwracająca nazwy państw do przedstawienia w formularzu. """
    return [(c.location.pk, c.location.name) for c in Country.objects.all()]


class LocationForm(forms.ModelForm):
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
    parent = forms.ChoiceField(
        required = False,
        choices = get_country_names(),
        label = _('Parent'),
        widget = forms.Select(attrs={'class': 'form-control'})
    )
    description = forms.CharField(
        required = False,
        max_length = 10000,
        label = _('Description'),
        widget = forms.Textarea(attrs={'class': 'form-control'})
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

    class Meta:
        model = Location
        fields = ('name', 'description', 'country_code', 'parent', 'population',
                  'latitude', 'longitude', 'image',)

    def clean(self):
        cleaned_data = super(LocationForm, self).clean()
        try:
            location = Location.objects.get(pk=self.cleaned_data['parent'])
        except Location.DoesNotExist:
            self._errors['parent'] = (_("Selected location does not exist"))
        self.cleaned_data['parent'] = location
        return cleaned_data


class IdeaLocationForm(forms.ModelForm):
    """
    Custom form for Idea - autocomplete value of location field.
    """
    name = forms.CharField(
        required = True,
        max_length = 64,
        widget = forms.TextInput(attrs={'class': 'form-control'})
    )
    description = forms.CharField(
        required = False,
        max_length = 20480,
        widget = forms.Textarea(attrs={'class': 'form-control'})
    )
    category = forms.ModelChoiceField(
        required = False,
        queryset = IdeaCategory.objects.all(),
        widget = forms.Select(attrs={'class': 'form-control'})
    )
    location = forms.ModelChoiceField(
        required = True,
        queryset = Location.objects.all(),
        widget = forms.HiddenInput()
    )
    tags = TagField()

    class Meta:
        model = Idea
        fields = ('name', 'description', 'location', 'tags', 'category',)


class NewsLocationForm(forms.ModelForm):
    """
    Custom form for Idea - autocomplete value of location field.
    """
    title = forms.CharField(
        widget = forms.TextInput(attrs={'class': 'form-control'})
    )
    content = forms.CharField(
        required = False,
        max_length = 10248,
        widget = forms.Textarea(attrs={'class': 'form-control'})
    )
    category = forms.ModelChoiceField(
        required = False,
        queryset = BlogCategory.objects.all(),
        widget = forms.Select(attrs={'class': 'form-control'})
    )
    location = forms.ModelChoiceField(
        required = True,
        queryset = Location.objects.all(),
        widget = forms.HiddenInput()
    )
    tags = TagField(required=False)

    class Meta:
        model = News
        fields = ('title', 'content', 'category', 'location', 'tags')


class DiscussionLocationForm(forms.ModelForm):
    """
    Custom form for Discussion - autocomplete value of location field.
    """
    question = forms.CharField(
        widget = forms.TextInput(attrs={'class': 'form-control'})
    )
    intro = forms.CharField(
        max_length = 10248,
        widget = forms.Textarea(attrs={'class': 'form-control'})
    )
    category = forms.ModelChoiceField(
        queryset = ForumCategory.objects.all(),
        widget = forms.Select(attrs={'class': 'form-control'})
    )
    location = forms.ModelChoiceField(
        required = True,
        queryset = Location.objects.all(),
        widget = forms.HiddenInput()
    )
    tags = TagField(required=False)

    class Meta:
        model = Discussion
        fields = ('question', 'intro', 'category', 'location', 'tags')


class SearchDiscussionForm(SearchForm):
    """
    Formularz wyszukiwania dyskusji w bieżącej lokalizacji.
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
    Formularz do wysyłania zaproszeń innym użytkownikom.
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
