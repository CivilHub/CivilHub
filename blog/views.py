# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext as _
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.contenttypes.models import ContentType

from maps.forms import AjaxPointerForm
from maps.models import MapPointer
from locations.links import LINKS_MAP as links
from locations.models import Location
from locations.mixins import LocationContextMixin, SearchableListMixin
from places_core.mixins import LoginRequiredMixin
from places_core.permissions import is_moderator
from places_core.helpers import get_time_difference, sort_by_locale

from .models import Category, News
from .forms import NewsForm


class BlogContextMixin(LocationContextMixin):
    """ """
    def get_context_data(self, form=None, object=None):
        context = super(BlogContextMixin, self).get_context_data()
        context['links'] = links['news']
        if form is not None:
            context['form'] = form
        return context


class CategoryListView(ListView):
    """ Categories for place's blog. """
    model = Category


class CategoryDetailView(DetailView):
    """ Show category info. """
    model = Category


class CategoryCreateView(LoginRequiredMixin, CreateView):
    """ Create new category. """
    model = Category
    fields = ['name', 'description']


class NewsListView(BlogContextMixin, SearchableListMixin):
    """ List of projects for one place. """
    model = News
    paginate_by = 25

    def get_context_data(self):
        context = super(NewsListView, self).get_context_data()
        context['categories'] = Category.objects.all()
        return context

    def get_queryset(self):
        qs = super(NewsListView, self).get_queryset()
        return qs.filter(title__icontains=self.request.GET.get('haystack', ''))


class NewsDetailView(BlogContextMixin, DetailView):
    """ Detailed news page. """
    model = News

    def get_context_data(self, **kwargs):
        news = super(NewsDetailView, self).get_object()
        content_type = ContentType.objects.get_for_model(news)
        context = super(NewsDetailView, self).get_context_data(**kwargs)
        context['is_moderator'] = is_moderator(self.request.user, news.location)
        context['location'] = news.location
        context['content_type'] = content_type.pk
        context['title'] = news.title
        context['map_markers'] = MapPointer.objects.filter(
                content_type = ContentType.objects.get_for_model(self.object)
            ).filter(object_pk=self.object.pk)
        if self.request.user == self.object.creator:
            context['marker_form'] = AjaxPointerForm(initial={
                'content_type': ContentType.objects.get_for_model(self.object),
                'object_pk'   : self.object.pk,
            })
        context['links'] = links['news']
        return context


class NewsCreateView(LoginRequiredMixin, BlogContextMixin, CreateView):
    model = News
    form_class = NewsForm

    def get_initial(self):
        initial = super(NewsCreateView, self).get_initial()
        location_slug = self.kwargs.get('location_slug')
        if location_slug is not None:
            initial['location'] = get_object_or_404(Location, slug=location_slug)
        return initial

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.creator = self.request.user
        obj.save()
        form.save_m2m()
        try:
            for m in json.loads(self.request.POST.get('markers')):
                marker = MapPointer.objects.create(
                    content_type=ContentType.objects.get_for_model(News),
                    object_pk=obj.pk, latitude=m['lat'], longitude=m['lng'])
        except Exception:
            # FIXME: silent fail, powinna być flash message
            pass
        return super(NewsCreateView, self).form_valid(form)


class NewsUpdateView(LoginRequiredMixin, BlogContextMixin, UpdateView):
    """ Let owner edit his newses. """
    model = News
    form_class = NewsForm

    def get_context_data(self, **kwargs):
        context = super(NewsUpdateView, self).get_context_data(**kwargs)
        context['title'] = self.get_object().title
        context['subtitle'] = _('Edit entry')
        context['location'] = self.get_object().location
        return context
