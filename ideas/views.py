# -*- coding: utf-8 -*-
import json
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy
from django.contrib.contenttypes.models import ContentType
# Use generic django views
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
# Application native models
from models import Idea, Vote
# Activity stream
from actstream import action
from places_core.actstreams import idea_action_handler


def get_votes(idea):
    """
    Get total votes calculated
    """
    i = idea
    votes_total = Vote.objects.filter(idea=i)
    votes_up = len(votes_total.filter(vote=True))
    votes_down = len(votes_total.filter(vote=False))
    return votes_up - votes_down


class IdeasListView(ListView):
    """
    List all ideas
    """
    model = Idea
    context_object_name = 'ideas'


class IdeasDetailView(DetailView):
    """
    Detailed idea view
    """
    model = Idea
    def get_object(self):
        object = super(IdeasDetailView, self).get_object()
        try:
            object.votes = get_votes(object)
            content_type = ContentType.objects.get_for_model(Idea)
            object.content_type = content_type.pk
        except:
            object.votes = 'Brak votes'
        return object


class CreateIdeaView(CreateView):
    """
    Allow users to create new ideas
    """
    model = Idea
    fields = ['name', 'description', 'location']
    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super(CreateIdeaView, self).form_valid(form)


class UpdateIdeaView(UpdateView):
    """
    Update existing idea details
    """
    model = Idea
    fields = ['name', 'description', 'location']


class DeleteIdeaView(DeleteView):
    """
    Allow users to delete their ideas
    """
    model = Idea
    success_url = reverse_lazy('ideas:index')


def vote(request):
    """
    Make vote (up/down) on idea
    """
    if request.method == 'POST':
        v    = request.POST['vote']
        idea = Idea.objects.get(pk=request.POST['idea'])
        user = request.user
        votes_check = Vote.objects.filter(user=request.user).filter(idea=idea)
        if len(votes_check) > 0:
            response = {
                'success': False,
                'message': 'You voted already on this idea',
                'votes': get_votes(idea),
            }
        else:
            user_vote = Vote(
                user = user,
                idea = idea,
                vote = True if v == 'up' else False
            )
            user_vote.save()
            response = {
                'success': True,
                'message': 'Vote saved',
                'votes': get_votes(idea),
            }
            action.send(request.user, action_object=idea, verb='voted on')
        return HttpResponse(json.dumps(response))
