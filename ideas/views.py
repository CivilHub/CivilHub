# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from models import Idea, Vote

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
            object.votes = Vote.objects.get(idea=object.pk)
        except:
            object.votes = 'Brak votes'
        return object
    
class CreateIdeaView(CreateView):
    """
    Allow users to create new ideas
    """
    model = Idea
    fields = ['name', 'description', 'location']
    
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
        user_vote = Vote(
            user = user,
            idea = idea,
            vote = True if v == 'up' else False
        )
        user_vote.save()
        return HttpResponse('Vote saved')
