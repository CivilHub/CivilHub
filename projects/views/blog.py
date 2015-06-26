# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404, render
from django.views.generic import View
from django.views.generic.detail import SingleObjectMixin

from places_core.helpers import ct_for_obj
from places_core.mixins import LoginRequiredMixin
from simpleblog.forms import BlogEntryForm
from simpleblog.models import BlogEntry

from ..models import SocialProject
from ..permissions import check_access


class ProjectBlogMixin(SingleObjectMixin, View):
    model = SocialProject

    def dispatch(self, *args, **kwargs):
        self.object = self.get_object()
        return super(ProjectBlogMixin, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProjectBlogMixin, self).get_context_data(**kwargs)
        context.update({
            'object': self.object,
            'location': self.object.location,
            'project_access': check_access(self.object, self.request.user), })
        return context


class ProjectNewsCreate(LoginRequiredMixin, ProjectBlogMixin):
    form_class = BlogEntryForm
    template_name = 'projects/news_form.html'

    def get(self, request, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(**kwargs)
        context['form'] = self.form_class(initial={
            'content_type': ct_for_obj(self.object),
            'object_id': self.object.pk,
        })
        return render(request, self.template_name, context)


class ProjectBlogList(ProjectBlogMixin):
    """ """
    template_name = 'projects/news_list.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectBlogList, self).get_context_data(**kwargs)
        context['object_list'] = BlogEntry.objects.get_published_in(self.object)
        return context

    def get(self, request, **kwargs):
        return render(request, self.template_name, self.get_context_data())


class ProjectBlogDetail(ProjectBlogMixin):
    template_name = 'projects/news_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ProjectBlogDetail, self).get_context_data(**kwargs)
        context.update({
            'news': get_object_or_404(BlogEntry, pk=self.kwargs.get('news_pk')), })
        return context

    def get(self, request, **kwargs):
        return render(request, self.template_name, self.get_context_data(**kwargs))
