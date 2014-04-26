# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from models import Location

class LocationListView(ListView):
    """
    Location list
    """
    model = Location
    context_object_name = 'locations'
    template_name = 'location_list.html'
    def get_context_data(self, **kwargs):
        context = super(LocationListView, self).get_context_data(**kwargs)
        context['title'] = 'Locations'
        return context
        
class LocationDetailView(DetailView):
    """
    Detailed location view
    """
    model = Location
        
class CreateLocationView(CreateView):
    """
    Add new location
    """
    model = Location
    fields = ['name', 'description', 'latitude', 'longitude', 'image']
    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super(CreateLocationView, self).form_valid(form)
    
class UpdateLocationView(UpdateView):
    """
    Update existing location
    """
    model = Location
    fields = ['name', 'description', 'latitude', 'longitude', 'image']
    
class DeleteLocationView(DeleteView):
    """
    Delete location
    """
    model = Location
    success_url = reverse_lazy('locations:index')
