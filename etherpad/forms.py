# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from .client import EtherpadException, EtherpadLiteClient
from .models import Pad


class ServePadForm(forms.Form):
    """ Form to display inline directly on detail page. """
    # For now there is only .txt format available.
    # Support for more formats will come soon.
    FORMAT_CHOICES = (
        ('.txt', 'TXT'),
    )

    file_format = forms.ChoiceField(choices=FORMAT_CHOICES, label=_(u"save as"))
    pad = forms.ModelChoiceField(queryset=Pad.objects.all(),
        widget=forms.HiddenInput())


class PadCreationForm(forms.ModelForm):
    """ Front-end form allowing registered users create new pads for their groups. """
    class Meta:
        model = Pad
        exclude = ('slug',)

    def clean(self):
        """ We have to be sure that pad name does not exist yet. """
        cleaned_data = super(PadCreationForm, self).clean()
        group = cleaned_data.get('group')
        pad_id = u"{}${}".format(group.etherpad_id,
            cleaned_data.get('name').replace(' ', '_'))
        client = EtherpadLiteClient(
            base_params={'apikey': settings.ETHERPAD_API_KEY},
            base_url=settings.ETHERPAD_INTERNAL_URL)
        response = client.listPads(groupID=group.etherpad_id)
        if pad_id in response['padIDs']:
            self.add_error('name', _(u"Name already exists"))
        return cleaned_data
