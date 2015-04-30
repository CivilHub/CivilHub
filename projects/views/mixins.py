# -*- coding: utf-8 -*-
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404

from locations.mixins import LocationContextMixin
from locations.models import Location
from places_core.mixins import LoginRequiredMixin

from ..models import SocialProject
from ..permissions import check_access


class ProjectContextMixin(LocationContextMixin):
    """ A mixin for forms that create tasks and groups of tasks. """

    def get_context_data(self, form=None):
        group_id = self.kwargs.get('group_id')
        project_slug = self.kwargs.get('slug')
        location_slug = self.kwargs.get('location_slug')
        context = super(ProjectContextMixin, self).get_context_data(form)
        context['form'] = form
        if project_slug is not None:
            context['object'] = get_object_or_404(SocialProject,
                                                  slug=project_slug)
            context['project_access'] = check_access(context['object'],
                                                     self.request.user)
        if location_slug is not None:
            context['location'] = get_object_or_404(Location,
                                                    slug=location_slug)
        return context


class ProjectAccessMixin(LoginRequiredMixin, ProjectContextMixin):
    """ We check whether the user has the proper access rights. """

    def get(self, request,
            location_slug=None,
            slug=None,
            group_id=None,
            task_id=None):
        # TODO: We can show something more appropriate than 403.
        if not check_access(self.get_object(), request.user):
            raise PermissionDenied
        return super(ProjectAccessMixin, self).get(request)

    def post(self, request,
             slug=None,
             location_slug=None,
             group_id=None,
             task_id=None):
        if not check_access(self.get_object(), request.user):
            raise PermissionDenied
        return super(ProjectAccessMixin, self).post(request)
