# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.utils.translation import ugettext as _
from locations.models import Location

class LocationForm(ModelForm):
    """
    Edit/update/create location form
    """
    class Meta:
        model = Location
