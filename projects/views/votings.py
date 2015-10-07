# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from rest_framework.renderers import JSONRenderer

from mapvotes.forms import VotingForm
from mapvotes.models import Voting
from mapvotes.serializers import MarkerSerializer
from places_core.mixins import LoginRequiredMixin
from ..models import SocialProject
from ..permissions import check_access


class ProjectMixin(object):
    """ Provides common context for views related to projects.

    WARNING: because of template variables naming conventions, keyword
    ``object``, normally used by Django, is reserved exclusively for
    ``SocialProject`` model instances.
    """
    def dispatch(self, request, *args, **kwargs):
        if not hasattr(self, 'project'):
            self.project = get_object_or_404(SocialProject,
                                             slug=kwargs.get('project_slug'))
        return super(ProjectMixin, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProjectMixin, self).get_context_data(**kwargs)
        context.update({
            'object': self.project,
            'location': self.project.location,
            'project_access': check_access(self.project, self.request.user)})
        return context


class ProjectAccessMixin(LoginRequiredMixin, ProjectMixin):
    """ Check for user permissions in edit and create views.
    """
    def dispatch(self, request, *args, **kwargs):
        self.project = get_object_or_404(SocialProject,
                                         slug=kwargs.get('project_slug'))
        if not check_access(self.project, self.request.user):
            raise PermissionDenied
        return super(ProjectAccessMixin, self).dispatch(request, *args, **kwargs)


class VotingCreateView(ProjectAccessMixin, CreateView):
    """ Create new voting. Related fields will be filled automatically.
    """
    model = Voting
    context_object_name = 'voting'
    template_name = 'projects/voting_form.html'
    form_class = VotingForm

    def get_form_kwargs(self):
        kwargs = super(VotingCreateView, self).get_form_kwargs()
        kwargs.update({
            'request': self.request,
            'content_object': self.project,})
        return kwargs

    def get_success_url(self):
        return reverse('projects:voting-markers', kwargs={
            'pk': self.object.pk, 'project_slug': self.project.slug})


class VotingUpdateView(ProjectAccessMixin, UpdateView):
    """ Update existing ``Voting`` instance.
    """
    model = Voting
    context_object_name = 'voting'
    template_name = 'projects/voting_form.html'
    form_class = VotingForm

    def dispatch(self, request, *args, **kwargs):
        # We have to be sure that updated instance belongs to currently
        # active project to avoid "permission clash".
        self.project = get_object_or_404(SocialProject,
                                         slug=kwargs.get('project_slug'))
        self.object = self.get_object()
        if not self.project == self.object.content_object:
            raise Http404
        return super(VotingUpdateView, self).dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(VotingUpdateView, self).get_form_kwargs()
        kwargs.update({
            'request': self.request,
            'content_object': self.project,})
        return kwargs

    def get_success_url(self):
        return self.object.get_absolute_url()

    def get_context_data(self, **kwargs):
        context = super(VotingUpdateView, self).get_context_data(**kwargs)
        context.update({'update': True})
        return context


class VotingDeleteView(ProjectAccessMixin, DeleteView):
    """ Delete existing voting along with all markers.
    """
    model = Voting
    context_object_name = 'voting'
    template_name = 'projects/voting_delete_confirm.html'

    def get_success_url(self):
        return reverse('projects:settings', kwargs={
                       'slug': self.project.slug})


class VotingSummaryView(ProjectMixin, DetailView):
    """ Show summary for all markers included in selected voting.
    """
    model = Voting
    context_object_name = 'voting'
    template_name = 'projects/voting_summary.html'

    def get_context_data(self, **kwargs):
        context = super(VotingSummaryView, self).get_context_data(**kwargs)
        context['markers'] = self.object.markers.annotate(
            vote_count=Count('votes')).order_by('-vote_count')
        return context


class VotingMapMixin(DetailView):
    """ Mixin providing JSON serialized markers for map.
    """
    model = Voting
    context_object_name = 'voting'

    def get_context_data(self, **kwargs):
        """ Serializes values for scripts. """
        serializer = MarkerSerializer(self.object.markers.all(), many=True,
                                      context={'request': self.request})
        context = super(VotingMapMixin, self).get_context_data(**kwargs)
        context.update({'markers': JSONRenderer().render(serializer.data)})
        return context


class VotingDetailView(ProjectMixin, VotingMapMixin):
    """ Show details for given voting along with map with markers.

    This is the main view meant for front-end users.
    """
    template_name = 'projects/voting_details.html'

    def get_context_data(self, **kwargs):
        context = super(VotingDetailView, self).get_context_data(**kwargs)
        enabled = self.request.user.is_authenticated()
        if not self.object.is_active():
            enabled = False
        context.update({'user_can_vote': enabled,})
        return context


class VotingMarkersView(ProjectMixin, VotingMapMixin):
    """ Add, delete or edit markers for selected voting.
    """
    template_name = 'projects/voting_markers.html'

    def dispatch(self, request, *args, **kwargs):
        self.project = get_object_or_404(SocialProject,
                                         slug=kwargs.get('project_slug'))
        self.object = self.get_object()
        if not check_access(self.project, request.user):
            if not self.object.is_public or request.user.is_anonymous():
                raise PermissionDenied
        return super(VotingMarkersView, self).dispatch(request, *args, **kwargs)

