# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.views.generic.base import ContextMixin
from django.db.models import FieldDoesNotExist

from rest_framework import viewsets

from places_core.helpers import get_time_difference
from places_core.permissions import is_moderator
from .models import Location


class LocationContentMixin(viewsets.ModelViewSet):
    """ We allow for filtering of content with locations in mind"""
    def get_queryset(self):
        qs = super(LocationContentMixin, self).get_queryset()
        try:
            location_pk = int(self.request.QUERY_PARAMS.get('pk'))
            return qs.filter(location__pk=int(location_pk))
        except Exception:
            return qs

    def pre_save(self, obj):
        obj.creator = self.request.user


class DateFilteredContentMixin(viewsets.ModelViewSet):
    """ Filtering based on defined time intervals."""
    def get_queryset(self):
        qs = super(DateFilteredContentMixin, self).get_queryset()
        time = get_time_difference(self.request.QUERY_PARAMS.get('time'))
        if time is not None:
            return qs.filter(date_created__gt=time)
        return qs


class CategoryFilteredContentMixin(viewsets.ModelViewSet):
    """ Filtering through category"""
    def get_queryset(self):
        qs = super(CategoryFilteredContentMixin, self).get_queryset()
        try:
            category_pk = int(self.request.QUERY_PARAMS.get('category'))
            return qs.filter(category__pk=category_pk)
        except Exception:
            return qs


class ContentMixin(LocationContentMixin,
                   DateFilteredContentMixin,
                   CategoryFilteredContentMixin):
    """
    A combinated mixin for all EST API views that present the content
    within one location.
    """
    pass


class LocationContextMixin(ContextMixin):
    """ We complete the context in the views connected with the location."""
    def get_current_location (self):
        location_slug = self.kwargs.get('location_slug')
        return get_object_or_404(Location, slug=location_slug)

    def get_context_data(self, object=None, form=None):
        context = super(LocationContextMixin, self).get_context_data()
        location_slug = self.kwargs.get('location_slug')
        if location_slug is not None:
            location = get_object_or_404(Location, slug=location_slug)
            context.update({
                'location': location,
                'is_moderator': is_moderator(self.request.user, location),
            })
            self.location = location
        return context


class SearchableListMixin(ListView):
    """ A mixin that allows to look through a list views."""
    def get_queryset(self):
        # We narrow the results to only one location
        location_slug = self.kwargs.get('location_slug')
        if location_slug is None:
            qs = self.model.objects.all()
        else:
            l = get_object_or_404(Location, slug=location_slug)
            id_list = [l.pk, ] + [x[0] for x in l.location_set.values_list('pk')]
            qs = self.model.objects.filter(location__pk__in=id_list)

        # We filter results only within one category
        try:
            category_pk = int(self.request.GET.get('category'))
        except (ValueError, TypeError):
            category_pk = None
        if category_pk is not None:
            qs = qs.filter(category__pk=category_pk)

        # We set a maximum time period we want to search...
        time_limit = get_time_difference(self.request.GET.get('time', 'all'))
        if time_limit is not None:
            qs = qs.filter(date_created__gte=time_limit)

        # ...and the order of results displayed.
        order = self.request.GET.get('sortby', '-date_created')
        try:
            self.model._meta.get_field_by_name(order.replace('-', ''))
            qs = qs.order_by(order)
        except FieldDoesNotExist:
            pass

        return qs
