# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.views.generic.list import ListView
from models import Location

class LocationListView(ListView):
    """
    Location list
    """
    model = Location
    
    def get_context_data(self, **kwargs):
        context = super(LocationListView, self).get_context_data(**kwargs)
        context['title'] = 'Locations'
        return context
