# -*- coding: utf-8 -*-
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _

from locations.models import Location
from places_core.forms import BootstrapBaseForm

from .models import ContentObjectGallery, ContentObjectPicture, \
                    UserGalleryItem, LocationGalleryItem


class BackgroundForm(forms.Form, BootstrapBaseForm):
    """
    Form allows users to select / crop the image background for the profile.
    """
    image = forms.ImageField(
        label=_("Image"),
        widget=forms.FileInput(attrs={'title': _("Choose picture")}))
    x = forms.IntegerField(widget=forms.HiddenInput())
    y = forms.IntegerField(widget=forms.HiddenInput())
    x2 = forms.IntegerField(widget=forms.HiddenInput())
    y2 = forms.IntegerField(widget=forms.HiddenInput())


class UserItemForm(forms.ModelForm, BootstrapBaseForm):
    """
    Form to add / edit images in user gallery's.
    """
    image = forms.ImageField(label=u'', required=True)
    name = forms.CharField(
        required=False,
        label=_("Name"),
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(
        required=False,
        label=_("Description"),
        widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = UserGalleryItem
        fields = ('image', 'name', 'description', )


class SimpleItemForm(forms.ModelForm, BootstrapBaseForm):
    """ Simplified form to edit the metadata of the photo. """
    name = forms.CharField(
        required=False,
        label=_("Name"),
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(
        required=False,
        label=_("Description"),
        widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = UserGalleryItem
        fields = ('name', 'description', )


class LocationItemForm(forms.ModelForm, BootstrapBaseForm):
    """
    Form to add photos to the gallery location.
    """
    image = forms.ImageField(label=u'', required=True)
    name = forms.CharField(
        required=False,
        label=_("Name"),
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(
        required=False,
        label=_("Description"),
        widget=forms.Textarea(attrs={'class': 'form-control'}))
    location = forms.ModelChoiceField(required=True,
                                      queryset=Location.objects.all(),
                                      widget=forms.HiddenInput())

    class Meta:
        model = LocationGalleryItem
        fields = ('image', 'name', 'description', 'location', )


class ContentGalleryForm(forms.ModelForm):
    """ Form for new kind of galleries universal for all models.
    """
    class Meta:
        model = ContentObjectGallery
        exclude = ('dirname', )
        widgets = {
            'content_type': forms.HiddenInput(),
            'object_id': forms.HiddenInput(),
        }


class PictureUpdateForm(forms.ModelForm):
    """ Simplified form for updating ContentObjectPicture instances.
    """
    class Meta:
        model = ContentObjectPicture
        fields = ('name', 'description', )
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }


class PictureUploadForm(forms.ModelForm):
    """ Unified form for uploading pictures.
    """
    class Meta:
        model = ContentObjectPicture
        exclude = ('uploaded_by', )
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'gallery': forms.HiddenInput(),
        }


class MassRemoveForm(forms.Form):
    """ Select gallery items to delete from handy list.
    """
    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance')
        super(MassRemoveForm, self).__init__(*args, **kwargs)
        self.fields['pictures'] = forms.ModelMultipleChoiceField(
            queryset=self.instance.pictures.all(),
            widget=forms.CheckboxSelectMultiple,
            label=_(u"Select images you wish to remove"))

    def is_valid(self):
        valid = super(MassRemoveForm, self).is_valid()
        if not valid:
            return valid
        for picture in self.cleaned_data['pictures']:
            picture.delete()
        return True
