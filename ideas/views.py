# -*- coding: utf-8 -*-
import json
from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import PermissionDenied
# Use generic django views
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.translation import ugettext as _
from actstream import action
# Application native models
from userspace.models import UserProfile
from models import Idea, Vote, Category
from forms import IdeaForm, CategoryForm
from maps.forms import AjaxPointerForm
from maps.models import MapPointer
from places_core.mixins import LoginRequiredMixin
# Custom comments
from comments.models import CustomComment
from places_core.permissions import is_moderator

def get_votes(idea):
    """
    Get total votes calculated
    """
    i = idea
    votes_total = Vote.objects.filter(idea=i)
    votes_up = len(votes_total.filter(vote=True))
    votes_down = len(votes_total.filter(vote=False))
    return votes_up - votes_down


def vote(request):
    """
    Make vote (up/down) on idea
    """
    if request.method == 'POST':
        v    = request.POST['vote']
        idea = Idea.objects.get(pk=request.POST['idea'])
        user = request.user
        prof = UserProfile.objects.get(user=user)
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
            prof.rank_pts += 1
            prof.save()
        return HttpResponse(json.dumps(response))


class CreateCategory(LoginRequiredMixin, CreateView):
    """
    Create new category for ideas.
    """
    model = Category
    template_name = 'ideas/category-create.html'
    form_class = CategoryForm
    success_url = '/'

    def get_context_data(self, **kwargs):
        if not self.request.user.is_superuser:
            return HttpResponseNotAllowed
        context = super(CreateCategory, self).get_context_data(**kwargs)
        context['title'] = _('Create new category')
        return context


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
            comment_set = CustomComment.objects.filter(
                content_type=content_type.pk
            )
            comment_set = comment_set.filter(object_pk=object.pk)
            object.comments = len(comment_set)
        except:
            object.votes = _('no votes yet')
        return object

    def get_context_data(self, **kwargs):
        context = super(IdeasDetailView, self).get_context_data(**kwargs)
        context['is_moderator'] = is_moderator(self.request.user, self.object.location)
        context['title'] = self.object.name
        context['location'] = self.object.location
        context['map_markers'] = MapPointer.objects.filter(
                content_type = ContentType.objects.get_for_model(self.object)
            ).filter(object_pk=self.object.pk)
        if self.request.user == self.object.creator:
            context['marker_form'] = AjaxPointerForm(initial={
                'content_type': ContentType.objects.get_for_model(self.object),
                'object_pk'   : self.object.pk,
            })
        return context


class CreateIdeaView(CreateView):
    """
    Allow users to create new ideas
    """
    model = Idea
    form_class = IdeaForm

    def get_context_data(self, **kwargs):
        context = super(CreateIdeaView, self).get_context_data(**kwargs)
        context['title'] = _('create new idea')
        context['action'] = 'create'
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.creator = self.request.user
        obj.save()
        # Without this next line the tags won't be saved.
        form.save_m2m()
        return super(CreateIdeaView, self).form_valid(form)


class UpdateIdeaView(UpdateView):
    """
    Update existing idea details
    """
    model = Idea
    form_class = IdeaForm

    def get_context_data(self, **kwargs):
        context = super(UpdateIdeaView, self).get_context_data(**kwargs)
        context['is_moderator'] = is_moderator(self.request.user, self.object.location)
        if self.object.creator != self.request.user and not context['is_moderator']:
            raise PermissionDenied
        context['title'] = self.object.name
        context['action'] = 'update'
        return context


class DeleteIdeaView(DeleteView):
    """
    Allow users to delete their ideas (or not? Still not working).
    """
    model = Idea
    success_url = reverse_lazy('ideas:index')
