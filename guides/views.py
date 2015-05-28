# -*- coding: utf-8 -*-
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import ugettext as _
from django.views.generic import DetailView, View
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import DeleteView

from locations.mixins import LocationContextMixin
from places_core.mixins import LoginRequiredMixin

from .forms import GuideForm, GuideEditorsForm
from .models import Guide, GuideCategory, GuideTag


class GuideAccessMixin(SingleObjectMixin):
    """ Control access to update and delete views.
    """
    model = Guide

    def dispatch(self, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.has_access(self.request.user):
            raise PermissionDenied
        return super(GuideAccessMixin, self).dispatch(*args, **kwargs)


class GuideCreateView(LoginRequiredMixin, LocationContextMixin, View):
    """ Create new guide.
    """
    template_name = 'guides/guide_form.html'
    form_class = GuideForm

    def get(self, request, **kwargs):
        context = super(GuideCreateView, self).get_context_data()
        context['form'] = self.form_class()
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        self.location = self.get_current_location()
        form = self.form_class(request.POST)
        if not form.is_valid():
            context = super(GuideCreateView, self).get_context_data()
            context['form'] = form
            return render(request, self.template_name, context)
        guide = form.save(commit=False)
        guide.owner = request.user
        guide.location = self.location
        guide.save()
        guide.authors.add(request.user)
        form.save_m2m()
        return redirect(guide.get_absolute_url())


class GuideUpdateView(LoginRequiredMixin, LocationContextMixin, GuideAccessMixin, View):
    """ Update existing guide object. Limit things user can change.
    """
    template_name = 'guides/guide_form.html'
    form_class = GuideForm

    def get(self, request, **kwargs):
        context = super(GuideUpdateView, self).get_context_data()
        context['form'] = self.form_class(instance=self.object)
        return render(request, self.template_name, context)

    def post(self, request, **kwargs):
        self.location = self.get_current_location()
        form = self.form_class(request.POST, instance=self.object)
        if not form.is_valid():
            context = super(GuideUpdateView, self).get_context_data()
            context['form'] = form
            return render(request, self.template_name, context)
        guide = form.save(commit=False)
        guide.save()
        if not request.user in guide.authors.all():
            guide.authors.add(request.user)
        form.save_m2m()
        return redirect(guide.get_absolute_url())


class GuideDeleteView(LocationContextMixin, GuideAccessMixin, DeleteView):
    """ Owners may delete guides they have created.
    """
    model = Guide

    def get_success_url(self):
        return reverse('guides:list',
            kwargs={'location_slug': self.object.location.slug, })


class GuideListView(LocationContextMixin, View):
    """ List all guides for particular location.
    """
    model = Guide
    template_name = 'guides/guide_list.html'

    def get(self, request, **kwargs):
        self.location = self.get_current_location()
        context = super(GuideListView, self).get_context_data()
        if not self.location.guides.count():
            context['guides_empty'] = True
        context['location_set'] = [self.location, ]
        for parent in self.location.parents():
            if len(parent.guides.filter(status=2)):
                context['location_set'].append(parent)
        return render(request, self.template_name, context)


class GuideTagFilteredListView(LocationContextMixin, View):
    """ List guides by tags coming from same location.
    """
    model = Guide
    template_name = 'guides/guide_filtered_list.html'

    def get(self, request, **kwargs):
        tag = get_object_or_404(GuideTag, pk=kwargs.get('tag_pk'))
        self.location = self.get_current_location()
        context = super(GuideTagFilteredListView, self).get_context_data()
        context.update({
            'title': _(u"Guides tagged by"),
            'filter_object': tag,
            'object_list': [x for x in self.location.guides.all()\
                            if tag in x.tags.all()], })
        return render(request, self.template_name, context)


class GuideCategoryFilteredListView(LocationContextMixin, View):
    """ List guides filtered by category in particular location.
    """
    model = Guide
    template_name = 'guides/guide_filtered_list.html'

    def get(self, request, **kwargs):
        category = get_object_or_404(GuideCategory, pk=kwargs.get('category_pk'))
        self.location = self.get_current_location()
        context = super(GuideCategoryFilteredListView, self).get_context_data()
        context.update({
            'title': _(u"Guides in category"),
            'filter_object': category,
            'object_list': self.location.guides.filter(category=category), })
        return render(request, self.template_name, context)


class GuideDetailedViewMixin(LocationContextMixin, DetailView):
    """ Simple mixin for detailed views and sub-views.
    """
    model = Guide

    def get_context_data(self, **kwargs):
        context = super(GuideDetailedViewMixin, self).get_context_data()
        context['guide_access'] = self.object.has_access(self.request.user)
        return context


class GuideDetailView(GuideDetailedViewMixin):
    """ Show single guide article in particular location.
    """
    template_name = 'guides/guide_detail.html'


class GuideEditorsListView(GuideDetailedViewMixin):
    """ Show all editors of this guide and allow authorized users to add/remove them.
    """
    template_name = 'guides/guide_editors.html'
    form_class = GuideEditorsForm

    def dispatch(self, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.has_access(self.request.user):
            raise PermissionDenied
        return super(GuideEditorsListView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(GuideEditorsListView, self).get_context_data(**kwargs)
        context['form'] = self.form_class(instance=self.object)
        return context

    def post(self, request, **kwargs):
        form = self.form_class(request.POST, instance=self.object)
        if not form.is_valid():
            context = self.get_context_data()
            context['form'] = form
            return render(request, self.template_name, context)
        obj = form.save()
        return redirect(reverse('guides:editors', kwargs={
            'location_slug': self.object.location.slug,
            'slug': self.object.slug, }))


class EditorDeleteView(LoginRequiredMixin, GuideAccessMixin, View):
    """ Allow owner and users with proper access rights to manage editors.
    """
    def post(self, request, **kwargs):
        user = self.object.editors.get(pk=request.POST.get('user_id'))
        self.object.editors.remove(user)
        self.object.save()
        return redirect(reverse('guides:editors', kwargs={
            'location_slug': self.object.location.slug,
            'slug': self.object.slug, }))
