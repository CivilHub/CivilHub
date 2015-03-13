# -*- coding: utf-8 -*-
import json, datetime
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django.http import HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
# Use generic django views
from django.views.generic import View, DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils.translation import ugettext as _
from django.utils.timesince import timesince
from actstream import action
# Application native models
from userspace.models import UserProfile
from models import Idea, Vote, Category
from forms import IdeaForm, CategoryForm
from maps.forms import AjaxPointerForm
from maps.models import MapPointer
from locations.models import Location
from locations.mixins import LocationContextMixin
from locations.links import LINKS_MAP as links
from places_core.mixins import LoginRequiredMixin
from places_core.helpers import SimplePaginator, truncatehtml, get_time_difference
# Custom comments
from comments.models import CustomComment
# Custom permissions
from places_core.permissions import is_moderator


class IdeasContextMixin(LocationContextMixin):
    """
    Zapewnia dodatkowe zmienne w kontekście powiązane z lokalizacją obiektu/ów.
    """
    def get_context_data(self):
        context = super(IdeasContextMixin, self).get_context_data()
        context['links'] = links['ideas']
        return context


def vote(request):
    """ Make vote (up/down) on idea. """
    if request.method == 'POST':
        idea = Idea.objects.get(pk=request.POST['idea'])
        votes_check = Vote.objects.filter(user=request.user).filter(idea=idea)
        if len(votes_check) > 0:
            response = {
                'success': False,
                'message': _('You voted already on this idea'),
                'votes': idea.get_votes(),
            }
        else:
            user_vote = Vote(
                user = request.user,
                idea = idea,
                vote = True if request.POST.get('vote') == 'up' else False
            )
            user_vote.save()
            response = {
                'success': True,
                'message': _('Vote saved'),
                'votes': idea.get_votes(),
            }
            action.send(
                request.user,
                action_object=idea,
                verb= _('voted on'),
                vote = True if request.POST.get('vote') == 'up' else False
            )
            request.user.profile.rank_pts += 1
            request.user.profile.save()
        return HttpResponse(json.dumps(response), content_type="application/json")


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


class IdeasListView(IdeasContextMixin, ListView):
    """ List all ideas """
    model = Idea
    paginate_by = 15

    def get_queryset(self):
        location_slug = self.kwargs.get('location_slug')
        if location_slug is None:
            qs = self.model.objects.all()
        else:
            qs = self.model.objects.filter(location__slug=location_slug)
        haystack = self.request.GET.get('haystack')
        if haystack is not None:
            qs = qs.filter(name__icontains=haystack)
        time_limit = get_time_difference(self.request.GET.get('time', 'all'))
        if time_limit is not None:
            qs = qs.filter(date_created__gte=time_limit)
        order = self.request.GET.get('order', '-date_created')
        return qs.order_by(order)


class IdeasDetailView(DetailView):
    """ Detailed idea view. """
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
        context['title'] = self.object.name + " | " + self.object.location.name + " | CivilHub"
        context['location'] = self.object.location
        context['links'] = links['ideas']
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
        obj.edited = False
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
    template_name = 'locations/location_idea_form.html'

    def get_context_data(self, **kwargs):
        context = super(UpdateIdeaView, self).get_context_data(**kwargs)
        context['is_moderator'] = is_moderator(self.request.user, self.object.location)
        if self.object.creator != self.request.user and not context['is_moderator']:
            raise PermissionDenied
        context['location'] = self.object.location
        context['title'] = self.object.name
        context['action'] = 'update'
        context['links'] = links['ideas']
        return context

    def form_valid(self, form):
        form.instance.edited = True
        form.date_edited = timezone.now()
        return super(UpdateIdeaView, self).form_valid(form)
