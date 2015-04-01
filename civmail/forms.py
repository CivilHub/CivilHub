# -*- coding: utf-8 -*-
from django import forms
from django.utils.translation import ugettext_lazy as _

from locations.models import Location


class FollowersEmailForm(forms.Form):
    """ This form allows you to write and send messages to location's followers. """
    location_id = forms.IntegerField(widget=forms.HiddenInput())
    subject = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))

    def clean_location_id(self):
        data = self.cleaned_data['location_id']
        try:
            location = Location.objects.get(pk=data)
        except Location.DoesNotExist:
            raise forms.ValidationError(_(u"Selected location does not exist"))
        return data
