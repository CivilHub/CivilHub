# -*- coding: utf-8 -*-
import json
from urllib2 import unquote

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from haystack.query import SearchQuerySet
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .config import ABUSE_REASONS
from .serializers import ContentTypeSerializer, PaginatedSearchSerializer


class SearchResultsAPIViewSet(viewsets.ViewSet):
    """
    A serch enginge for the mobile application. It allows to check search results
    by specifing the correct entry for the search (of course in a url-friendly manner).
    It returns a list of found objects that contain the fields 'name', 'content_type'
    and 'object_pk'. The system recognizes phrases passed through such functions as
    'encodeURI', 'encodeURIComponent' or 'urlencode'.
    #### Sample query:
    ```/api-core/search/?q=warszawa```
    """
    serializer_class = PaginatedSearchSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def _get_model_labels(self, ct_list):
        if not len(ct_list):
            return None
        return [ContentType.objects.get(pk=x).model_class() for x in ct_list]

    def get_queryset(self):
        try:
            query_term = unquote(self.request.QUERY_PARAMS.get('q'))
            sqs = SearchQuerySet().filter(content=query_term)
            types = self.request.QUERY_PARAMS.get('ct', '').split(',')
            models = self._get_model_labels([int(x) for x in types if x])
            if models is not None:
                sqs = sqs.models(*models)
        except Exception:
            sqs = []
        return sqs

    def list(self, request):
        sqs = [x for x in self.get_queryset() if x.object is not None]
        paginator = Paginator(sqs, settings.LIST_PAGINATION_LIMIT)
        page = request.QUERY_PARAMS.get('page')
        try:
            results = paginator.page(page)
        except PageNotAnInteger:
            results = paginator.page(1)
        except EmptyPage:
            results = paginator.page(paginator.num_pages)
        serializer = self.serializer_class(results,
                                            context={'request': request})
        return Response(serializer.data)


class ContentTypeAPIViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A view that allows to download content ID types based on the application name
    or model and vice-versa. Only GET queries! By default all types are listed.

    It is possible to search in two ways, by adding GET parameters to the query:
        1. Pass an ID of a concrete content type (e.g. ?id=8)
        2. Pass the name of the application and model (e.g. ?app_label=ideas&model=idea)
    """
    queryset = ContentType.objects.all()
    serializer_class = ContentTypeSerializer
    paginate_by = None

    def get_queryset(self):
        app_label = self.request.QUERY_PARAMS.get('app_label', None)
        model = self.request.QUERY_PARAMS.get('model', None)
        id = self.request.QUERY_PARAMS.get('id', None)
        if id:
            return ContentType.objects.filter(pk=id)
        elif app_label and model:
            return ContentType.objects.filter(app_label=app_label, model=model)
        else:
            return ContentType.objects.all()


class AbuseReasonList(APIView):
    """ List of reasons to choose from for moderators, for egzample when they
        want to mark comment as hidden etc. This should be labels and values
        for some selector in modal-like form.
    """
    permission_classes = (permissions.AllowAny, )

    def get(self, request, **kwargs):
        return Response([{'value': x[0], 'label': unicode(x[1]), } for x in ABUSE_REASONS])
