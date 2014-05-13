# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext as _
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.contenttypes.models import ContentType
from .models import Category, News
from .forms import NewsForm
# Use our mixin to allow only some users make actions
from places_core.mixins import LoginRequiredMixin


class CategoryListView(ListView):
    """
    Categories for place's blog
    """
    model = Category
    context_object_name = 'categories'

    
class CategoryDetailView(DetailView):
    """
    Show category info
    """
    model = Category

    
class CategoryCreateView(LoginRequiredMixin, CreateView):
    """
    Create new category
    """
    model = Category
    fields = ['name', 'description']


class NewsListView(ListView):
    """
    News index for chosen location
    """
    model = News
    context_object_name = 'entries'

    
class NewsDetailView(DetailView):
    """
    Detailed news page
    """
    model = News

    def get_context_data(self, **kwargs):
        news = super(NewsDetailView, self).get_object()
        content_type = ContentType.objects.get_for_model(news)
        context = super(NewsDetailView, self).get_context_data(**kwargs)
        context['location'] = news.location
        context['content_type'] = content_type.pk
        context['title'] = news.title
        return context

    
class NewsCreateView(LoginRequiredMixin, CreateView):
    """
    Create new entry
    """
    model = News
    form_class = NewsForm

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super(NewsCreateView, self).form_valid(form)


class NewsUpdateView(LoginRequiredMixin, UpdateView):
    """
    Let owner edit his newses.
    """
    model = News
    form_class = NewsForm
    template_name = 'locations/location_news_form.html'

    def get_context_data(self, **kwargs):
        obj = super(NewsUpdateView, self).get_object()
        if obj.creator != self.request.user:
            raise PermissionDenied
        context = super(NewsUpdateView, self).get_context_data(**kwargs)
        context['title'] = obj.title
        context['subtitle'] = _('Edit entry')
        return context
