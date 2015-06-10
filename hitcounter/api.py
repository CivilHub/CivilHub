# -*- coding: utf-8 -*-
import datetime

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.translation import ugettext as _

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
        time_diff = timezone.now() - datetime.timedelta(days=30)
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


class VisitGraphDataAPIView(APIView):
    """ Show counter info divided into daily periods.
    """
    permission_classes = (permissions.AllowAny, )

    def get(self, request, **kwargs):
        try:
            pk = int(request.QUERY_PARAMS.get('pk'))
            ct = int(request.QUERY_PARAMS.get('ct'))
        except (TypeError, ValueError, ):
            raise Http404
        content_type = get_object_or_404(ContentType, pk=ct)
        instance = content_type.get_object_for_this_type(pk=pk)

        all_visits = Visit.objects.filter(content_type=content_type,
                                        object_id=instance.pk).order_by('date')

        start_time = all_visits.first().date
        stop_time = timezone.now()

        results = []
        the_time = start_time
        # FIXME: I have no idea why, but it seems that there is even 24 hours
        # difference between different auto_add_now fields. So for now it works
        # fine for polls, but not, e.g. for ideas.
        while the_time < stop_time + datetime.timedelta(days=1):
            results.append(all_visits.filter(date__year=the_time.year,
                                             date__month=the_time.month,
                                             date__day=the_time.day).count())
            the_time = the_time + datetime.timedelta(days=1)

        return Response({
            'title': _(u"Visit counter for %s" % instance),
            'start_time': start_time,
            'results': results, })
