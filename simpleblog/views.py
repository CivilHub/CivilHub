# -*- coding: utf-8 -*-
from django.core.exceptions import PermissionDenied
from django.views.generic import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import BlogEntryForm
from .models import BlogEntry


class BlogEntryDetailView(DetailView):
    """
    Single blog entry page. This view should be used for entries that are not
    bind to other content. The rest should be shown in respective apps.
    """
    model = BlogEntry


class BlogEntryCreateView(CreateView):
    """
    Create new blog entry.
    """
    model = BlogEntry
    form_class = BlogEntryForm

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user
        return super(BlogEntryCreateView, self).form_valid(form)


class BlogEntryUpdateView(UpdateView):
    """
    Update news entry - available only for admins and instance creator.
    """
    model = BlogEntry
    form_class = BlogEntryForm

    def dispatch(self, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.has_access(self.request.user):
            raise PermissionDenied
        return super(BlogEntryUpdateView, self).dispatch(*args, **kwargs)


class BlogEntryDeleteView(DeleteView):
    """
    This should be accessible only by admnins and objects author.
    """
    model = BlogEntry

    def dispatch(self, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.has_access(self.request.user):
            raise PermissionDenied
        return super(BlogEntryDeleteView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        if hasattr(self.object.content_object, 'get_absolute_url'):
            return self.object.content_object.get_absolute_url()
        return self.object.author.profile.get_absolute_url()
