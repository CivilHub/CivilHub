# -*- coding: utf-8 -*-
from rest_framework import viewsets

class LocationContentMixin(viewsets.ModelViewSet):
    """ Umożliwiamy filtrowanie zawartości pod kątem lokalizacji. """
    def get_queryset(self):
        qs = super(LocationContentMixin, self).get_queryset()
        try:
            location_pk = int(self.request.QUERY_PARAMS.get('pk', 0))
            return qs.filter(location__pk=int(location_pk))
        except Exception:
            return qs

    def pre_save(self, obj):
        obj.creator = self.request.user
