# -*- coding: utf-8 -*-
import datetime

from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone

from actstream.models import following
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from activities.serializers import ActionObjectSerializer
from blog.models import News
from ideas.models import Idea
from locations.models import Location

from .models import Visit


class HotBoxAPIView(APIView):
    """ Presents list of last "hot items".
    """
    permission_classes = (permissions.AllowAny, )

    def get_queryset(self):
        uid = self.request.QUERY_PARAMS.get('uid')
        lid = self.request.QUERY_PARAMS.get('lid')
        time_diff = timezone.now() - datetime.timedelta(days=7)
        if lid is not None:
            location = get_object_or_404(Location, pk=lid)
            news_set = location.news_set.filter(date_created__gte=time_diff)
            idea_set = location.idea_set.filter(date_created__gte=time_diff)
        elif uid is not None:
            user = get_object_or_404(User, pk=uid)
            id_list = [x.pk for x in user.profile.followed_locations()]
            news_set = News.objects.filter(
                location__pk__in=id_list,
                date_created__gte=time_diff)
            idea_set = Idea.objects.filter(
                location__pk__in=id_list,
                date_created__gte=time_diff)
        else:
            raise Http404
        return sorted(list(news_set) + list(idea_set), reverse=True,
            key=lambda x: Visit.objects.count_for_object(x))[:5]

    def get(self, request, **kwargs):
        qs = self.get_queryset()
        serializers = []
        for itm in qs:
            serializers.append(ActionObjectSerializer(itm).data)
        return Response(serializers)
