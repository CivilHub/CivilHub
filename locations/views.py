# -*- coding: utf-8 -*-
import json
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext as _
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from models import Location
# Use our mixin to allow only some users make actions
from places_core.mixins import LoginRequiredMixin

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
      
class CreateLocationView(LoginRequiredMixin, CreateView):
    """
    Add new location
    """
    model = Location
    fields = ['name', 'description', 'latitude', 'longitude', 'image']
    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super(CreateLocationView, self).form_valid(form)
    
class UpdateLocationView(LoginRequiredMixin, UpdateView):
    """
    Update existing location
    """
    model = Location
    fields = ['name', 'description', 'latitude', 'longitude', 'image']
    
class DeleteLocationView(LoginRequiredMixin, DeleteView):
    """
    Delete location
    """
    model = Location
    success_url = reverse_lazy('locations:index')
    
def add_follower(request, pk):
    """
    Add user to locations followers
    """
    location = get_object_or_404(Location, pk=pk)
    user = request.user
    location.users.add(user)
    try:
        location.save()
        response = {
            'success': True,
            'message': _('You follow this location'),
        }
    except:
        response = {
            'success': False,
            'message': _('Something, somewhere went terribly wrong'),
        }
    return HttpResponse(json.dumps(response))
    
def remove_follower(request, pk):
    """
    Remove user from locations followers
    """
    location = get_object_or_404(Location, pk=pk)
    user = request.user
    location.users.remove(user)
    try:
        location.save()
        response = {
            'success': True,
            'message': _('You stop following this location'),
        }
    except:
        response = {
            'success': False,
            'message': _('Something, somewhere went terribly wrong'),
        }
    return HttpResponse(json.dumps(response))
