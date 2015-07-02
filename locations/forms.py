# -*- coding: utf-8 -*-
from django import forms
from django.forms.util import ErrorList
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
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
    """ Edit/update/create location form """
    parent = forms.IntegerField(
        label = _('Parent'),
        required = False,
        help_text = _("Choose parent location for your place. You can see which place is currently selected in grey box above."),
        widget = forms.TextInput()
    )

    def clean(self):
        cparent = self.cleaned_data.get('parent')

        # Allow superuser to create new and edit existing countries/regions
        if self.user is not None and self.user.is_superuser:
            if cparent is not None:
                self.cleaned_data['parent'] = Location.objects.get(pk=cparent)
            return self.cleaned_data

        if cparent is None:
            msg = _(u"You have to choose at least country and region locations")
            self._errors['parent'] = ErrorList([msg])
            del self.cleaned_data['parent']
        else:
            try:
                parent = Location.objects.get(pk=cparent)
                if parent.kind != 'country':
                    self.cleaned_data['parent'] = parent
                else:
                    msg = _(u"You have to select region parent location")
                    self._errors['parent'] = ErrorList([msg])
                    del self.cleaned_data['parent']
            except Location.DoesNotExist:
                msg = _(u"Selected location does not exist")
                self._errors['parent'] = ErrorList([msg])
                del self.cleaned_data['parent']
        return self.cleaned_data

    def __init__(self, user=None, *args, **kwargs):
        self.user = user
        super(LocationForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Location
        fields = ('name', 'description', 'parent', 'population', 'latitude', 'longitude',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'latitude': forms.TextInput(attrs={'class': 'form-control'}),
            'longitude': forms.TextInput(attrs={'class': 'form-control'}),
            'population': forms.NumberInput(attrs={'class': 'form-control'}),
        }


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
        fields = ('name', 'description', 'video_url', 'location', 'tags', 'category', 'image')


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


class InviteUsersByEmail(forms.Form):
    """
    Similar to above, but this form allows users to invite others by email,
    wether they are already registered or not.
    """
    emails = forms.CharField(label=_(u"Emails"),
        help_text=_(u"Enter email addresses separated with comma"),
        widget=forms.TextInput(attrs={'class': 'email-input',}))

    def clean_emails(self):
        emails = [x.strip() for x in self.cleaned_data['emails'].split(',')]
        for email in emails:
            try:
                validate_email(email)
            except ValidationError:
                raise ValidationError(_(u"At least one email address is invalid"))
        return emails
