# -*- coding: utf-8 -*-
import json
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext as _
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from ideas.models import Idea
from forms import IdeaLocationForm
from models import Location
# Use our mixin to allow only some users make actions
from places_core.mixins import LoginRequiredMixin
# Activity stream
from actstream.actions import follow, unfollow


class LocationNewsList(DetailView):
    """
    Location news page
    """
    model = Location
    template_name = 'locations/location_news.html'


class LocationIdeasList(DetailView):
    """
    Location ideas list
    """
    model = Location
    template_name = 'locations/location_ideas.html'


class LocationIdeaCreate(CreateView):
    """
    Create new idea in scope of currently selected location.
    """
    model = Idea
    form_class = IdeaLocationForm
    template_name = 'locations/location_idea_form.html'
    fields = ['name', 'description', 'tags']

    def get(self, request, *args, **kwargs):
        #super(LocationIdeaCreate, self).get(request, *args, **kwargs)
        slug = kwargs['slug']
        ctx = {
            'location': Location.objects.get(slug=slug),
            'form': IdeaLocationForm(initial={
                'location': Location.objects.get(slug=slug)
            })
        }
        return render(request, self.template_name, ctx)
        

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.creator = self.request.user
        obj.save()
        # Without this next line the tags won't be saved.
        form.save_m2m()
        return super(LocationIdeaCreate, self).form_valid(form)


class LocationFollowersList(DetailView):
    """
    Location followers list
    """
    model = Location
    template_name = 'locations/location_followers.html'


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
    def get_context_data(self, **kwargs):
        location = super(LocationDetailView, self).get_object()
        context = super(LocationDetailView, self).get_context_data(**kwargs)
        context['title'] = location.name
        return context


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
        follow(user, location, actor_only = False)
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
        unfollow(user, location)
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
