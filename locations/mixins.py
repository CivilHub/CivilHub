# -*- coding: utf-8 -*-
from django.shortcuts import get_object_or_404
from django.views.generic.base import ContextMixin

from rest_framework import viewsets

from places_core.helpers import get_time_difference
from places_core.permissions import is_moderator
from .models import Location


class LocationContentMixin(viewsets.ModelViewSet):
    """ Umożliwiamy filtrowanie zawartości pod kątem lokalizacji. """
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
    """ Filtrowanie na podstawie zdefiniowanych przedziałów czasowych. """
    def get_queryset(self):
        qs = super(DateFilteredContentMixin, self).get_queryset()
        time = get_time_difference(self.request.QUERY_PARAMS.get('time'))
        if time is not None:
            return qs.filter(date_created__gt=time)
        return qs


class CategoryFilteredContentMixin(viewsets.ModelViewSet):
    """ Filtrowanie poprzez kategorię. """
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
    Kombinowany mixin dla wszystkich widoków REST API prezentujących
    zawartość w ramach jednej lokalizacji.
    """
    pass


class LocationContextMixin(ContextMixin):
    """ Uzupełniamy kontekst w widokach powiązanych z lokalizacją. """
    def get_context_data(self, object=None, form=None):
        context = super(LocationContextMixin, self).get_context_data()
        location_slug = self.kwargs.get('location_slug')
        if location_slug is not None:
            location = get_object_or_404(Location, slug=location_slug)
            context.update({
                'location': location,
                'is_moderator': is_moderator(self.request.user, location),
            })
        return context
