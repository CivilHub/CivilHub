# -*- coding: utf-8 -*-
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from places_core.mixins import LoginRequiredMixin
from places_core.permissions import is_moderator

from .mixins import ProjectContextMixin
from ..forms import DiscussionAnswerForm, SocialForumCreateForm,\
                    SocialForumUpdateForm
from ..models import SocialForumTopic, SocialForumEntry, SocialProject
from ..permissions import check_access


class ProjectForumContextMixin(ProjectContextMixin):
    """ A mixin for discussion subpages for this project. """

    def get_context_data(self, form=None, **kwargs):
        context = super(ProjectForumContextMixin, self).get_context_data()
        project_slug = self.kwargs.get('project_slug')
        if project_slug is not None:
            context['object'] = get_object_or_404(SocialProject,
                                                  slug=project_slug)
            context['location'] = context['object'].location
            context['is_moderator'] = is_moderator(self.request.user,
                                                   context['location'])
        if form is not None:
            context['form'] = form
        discussion_slug = self.kwargs.get('discussion_slug')
        if discussion_slug is not None:
            context['discussion'] = get_object_or_404(SocialForumTopic,
                                                      slug=discussion_slug)
        return context


class ProjectForumUpdateMixin(LoginRequiredMixin, UpdateView,
                              ProjectForumContextMixin):
    """ A mixin for discussion edition forms and discussion entries. """

    def permission_check_(self):
        if not check_access(self.get_object(), self.request.user):
            raise PermissionDenied

    def get(self, request, project_slug=None, discussion_slug=None, pk=None):
        self.permission_check_()
        return super(ProjectForumUpdateMixin, self).get(request, project_slug,
                                                        discussion_slug)

    def post(self, request, project_slug=None, discussion_slug=None, pk=None):
        self.permission_check_()
        return super(ProjectForumUpdateMixin, self).post(request, project_slug,
                                                         discussion_slug)


class ProjectForumListView(ProjectForumContextMixin, ListView):
    """ A list of discussions within one project. """
    model = SocialForumTopic
    paginate_by = 25

    def get_queryset(self):
        qs = super(ProjectForumListView, self).get_queryset()
        project_slug = self.kwargs.get('project_slug')
        if project_slug is not None:
            qs = qs.filter(project__slug=project_slug)
        return qs


class ProjectForumDetailView(ProjectForumContextMixin, ListView):
    """ One discussion with answers. """
    model = SocialForumEntry
    paginate_by = 25

    def get_queryset(self):
        qs = super(ProjectForumDetailView, self).get_queryset()
        discussion_slug = self.kwargs.get('discussion_slug')
        if discussion_slug is not None:
            qs = qs.filter(topic__slug=discussion_slug)
        return qs

    def get_context_data(self):
        context = super(ProjectForumDetailView, self).get_context_data()
        discussion_slug = self.kwargs.get('discussion_slug')
        if discussion_slug is not None:
            context['answer_form'] = DiscussionAnswerForm(initial={
                'topic': context['discussion'],
                'creator': self.request.user,
            })
            context['project_access'] = check_access(
                context['discussion'].project, self.request.user)
        return context


class ProjectForumCreateView(LoginRequiredMixin, CreateView,
                             ProjectForumContextMixin):
    """ New discussion creation within a project. """
    model = SocialForumTopic
    form_class = SocialForumCreateForm

    def get_success_url(self):
        return self.object.get_absolute_url()

    def form_valid(self, form):
        form.instance.creator = self.request.user
        project_slug = self.kwargs.get('project_slug')
        if project_slug is not None:
            form.instance.project = get_object_or_404(SocialProject,
                                                      slug=project_slug)
        return super(ProjectForumCreateView, self).form_valid(form)


class ProjectForumUpdateView(ProjectForumUpdateMixin):
    """ Existing discussion edition. """
    model = SocialForumTopic
    form_class = SocialForumUpdateForm
    slug_url_kwarg = 'discussion_slug'


class ProjectForumDeleteView(LoginRequiredMixin, DeleteView,
                             ProjectForumContextMixin):
    """ Discussion deletion - only for admins and mods! """
    model = SocialForumTopic

    def get_success_url(self):
        return reverse('projects:discussions',
                       kwargs={'project_slug': self.object.project.slug})

    def post(self, request, pk=None):
        if not is_moderator(request.user, self.get_object().project.location):
            raise PermissionDenied
        return super(ProjectForumDeleteView, self).post(request, pk)


class ProjectForumAnswerCreateView(LoginRequiredMixin, CreateView,
                                   ProjectForumContextMixin):
    """ Discussion answer. """
    model = SocialForumEntry
    form_class = DiscussionAnswerForm

    def get_success_url(self):
        return self.object.topic.get_absolute_url()

    def get_initial(self):
        initial = super(ProjectForumAnswerCreateView, self).get_initial()
        discussion_slug = self.kwargs.get('discussion_slug')
        if discussion_slug is not None:
            initial['topic'] = get_object_or_404(SocialForumTopic,
                                                 slug=discussion_slug)
        initial['creator'] = self.request.user
        return initial

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super(ProjectForumAnswerCreateView, self).form_valid(form)


class ProjectForumAnswerUpdateView(ProjectForumUpdateMixin):
    """ Edition of your own discussion answers, possibly for admins. """
    model = SocialForumEntry
    form_class = DiscussionAnswerForm

    def get_success_url(self):
        return self.object.topic.get_absolute_url()


class ProjectForumAnswerDeleteView(LoginRequiredMixin, DeleteView,
                                   ProjectForumContextMixin):
    """ Discussion entries deletion - admins, mods and project owners. """
    model = SocialForumEntry

    def get_success_url(self):
        return self.object.topic.get_absolute_url()

    def post(self, request, pk=None):
        if not check_access(self.get_object().topic.project, request.user):
            raise PermissionDenied
        return super(ProjectForumAnswerDeleteView, self).post(request, pk)
