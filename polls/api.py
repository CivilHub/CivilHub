# -*- coding: utf-8 -*-
from django.http import Http404
from django.shortcuts import get_object_or_404

from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Poll
from .serializers import AnswerSetSerializer, TimelineSetSerializer


class AnswerSetMixin(APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, **kwargs):
        try:
            poll_pk = int(request.QUERY_PARAMS.get('pk'))
        except (TypeError, ValueError, ):
            raise Http404
        self.object = get_object_or_404(Poll, pk=poll_pk)
        serializer = self.serializer_class(self.object)
        return Response(serializer.data)


class AnswerSetAPIView(AnswerSetMixin):
    """ Answer sets for basic charts (answer summary).
    """
    serializer_class = AnswerSetSerializer


class AnswersInTimeAPIView(AnswerSetMixin):
    """ Fetch all answers to present on timeline graph.
    """
    serializer_class = TimelineSetSerializer
