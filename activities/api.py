# -*- coding: utf-8 -*-
import datetime
import json

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.translation import ugettext as _

from actstream.actions import follow, unfollow
from actstream.models import Action, following, actor_stream, target_stream
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from notifications.models import notify
from places_core.helpers import get_time_difference

from .serializers import ActionSerializer


def new_follower(follower, target_user):
    if follower == target_user:
        return False
    notify(follower, target_user,
        key="follower",
        verb="started following you")


class ActionGraphAPIView(APIView):
    """ Presents list of activities related to any object and divided to
        periods by one day long. This is intended to be displayed on chart.
        This view takes few parameters, and, if some errors occured or not all
        of them are given, it presents 404 istead of server error.

        Allowable parameters are:

        `ct` - Content type ID, like in every generic relation in application.<br>
        `pk` - ID of item in question. Related to the above (Generic Foreign Key)<br>
    """
    permission_classes = (permissions.AllowAny, )

    def dispatch(self, *args, **kwargs):
        try:
            ct = int(self.request.GET.get('ct'))
            pk = int(self.request.GET.get('pk'))
        except (TypeError, ValueError, ):
            raise Http404

        content_type = get_object_or_404(ContentType, pk=ct)
        try:
            self.object = content_type.get_object_for_this_type(pk=pk)
        except ObjectDoesNotExist:
            raise Http404

        return super(ActionGraphAPIView, self).dispatch(*args, **kwargs)

    def get(self, request, **kwargs):
        stream = target_stream(self.object).order_by('-timestamp')
        started = stream.last().timestamp
        current = started
        maximum = timezone.now() + datetime.timedelta(hours=12)
        counters = []
        while current < maximum:
            qs = stream.filter(timestamp__year=current.year,
                               timestamp__month=current.month,
                               timestamp__day=current.day)
            counters.append(qs.count())
            current += datetime.timedelta(days=1)
        return Response({
            'title': _(u"Actions timeline for ") + self.object.__unicode__(),
            'point_interval': 24 * 3600 * 1000,
            'date_started': started,
            'name': _(u"Activities"),
            'count': stream.count(),
            'results': counters, })


class ActivityViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Entry point for activity API. We can fetch actions for specific user or
    related to specific target. Returned queryset is based on 3 parameters:<br>
        `type` - "actor", "target" or "user"<br>
        `ct`   - Content Type ID for object in question<br>
        `pk`   - ID of selected object<br>
        `content` - content filter in form of &lt;app_label&gt;&lt;model&gt; pair
    """
    model = Action
    serializer_class = ActionSerializer
    paginate_by = 15
    request_object = None

    def content_filter(self):
        content_filter = self.request.QUERY_PARAMS.get('content', 'all')
        if content_filter == 'all':
            return None
        app_label, model = content_filter.split('.')
        return ContentType.objects.get(app_label=app_label, model=model).pk

    def date_filter(self):
        return get_time_difference(self.request.QUERY_PARAMS.get('time'))

    def get_queryset(self):
        stream_type = self.request.QUERY_PARAMS.get('type')
        try:
            content_type = int(self.request.QUERY_PARAMS.get('ct'))
            object_id = int(self.request.QUERY_PARAMS.get('pk'))
        except (TypeError, ValueError):
            return super(ActivityViewSet, self).get_queryset()
        ct = ContentType.objects.get(pk=content_type)
        self.request_object = ct.get_object_for_this_type(pk=object_id)
        if stream_type == 'actor':
            qs = actor_stream(self.request_object)
        elif stream_type == 'target':
            qs = target_stream(self.request_object)
        elif stream_type == 'ngo':
            qs = Action.objects.ngostream(self.request_object)
        elif stream_type == 'location':
            qs = Action.objects.location(self.request_object)
        else:
            qs = Action.objects.mystream(self.request_object)
        content_filter = self.content_filter()
        if content_filter is not None:
            qs = qs.filter(Q(action_object_content_type__pk=content_filter) |
                           Q(target_content_type__pk=content_filter))
        date_filter = self.date_filter()
        if date_filter is not None:
            qs = qs.filter(timestamp__gte=date_filter)
        return qs


class FollowObjectView(APIView):
    """
    This view allows registered users to follow/unfollow any object registered
    by activity stream. We have to pass 2 parameters:<br>
        `ct` - Content Type ID<br>
        `pk` - ID of selected object<br>
    GET request will return information about that selected object is already
    followed by user. Perform POST request to toggle follow/unfollow state.
    """
    permission_classes = (permissions.IsAuthenticated, )
    instance = None

    def get_object(self):
        try:
            ct = int(self.request.QUERY_PARAMS.get('ct'))
            pk = int(self.request.QUERY_PARAMS.get('pk'))
        except (TypeError, ValueError):
            raise Http404
        content_type = ContentType.objects.get(pk=ct)
        try:
            instance = content_type.get_object_for_this_type(pk=pk)
        except ObjectDoesNotExist:
            raise Http404
        return instance

    def get(self, request):
        self.instance = self.get_object()
        return Response(
            {'following': self.instance in following(request.user), })

    def post(self, request):
        self.instance = self.get_object()
        instance_name = self.instance._meta.model_name

        if not self.instance in following(request.user):
            try:
                follow(request.user, self.instance,
                       actor_only=False,
                       send_action=False)
                msg = _(u"You are following this %s" % instance_name)
                is_follower = True
            except ImproperlyConfigured as e:
                return Response({'success': False, 'message': str(e)})
            if instance_name == 'location':
                self.instance.users.add(request.user)
            elif instance_name == 'user':
                new_follower(request.user, self.instance)
        else:
            unfollow(request.user, self.instance)
            msg = _(u"You are no longer following this %s" % instance_name)
            is_follower = False
            if instance_name == 'location':
                self.instance.users.remove(request.user)

        return Response(
            {'success': True,
             'message': msg,
             'following': is_follower, })


class FollowAllAPIView(APIView):
    """ Mainly for "follow all" button on facebook friends page.
    """
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request, **kwargs):
        id_list = [int(x.strip()) for x in request.POST.get('id').split(',')]
        for user in User.objects.filter(id__in=id_list):
            if not user in following(request.user):
                follow(request.user, user, send_action=False)
                new_follower(request.user, user)
        message = _(u"You have started following your friends!")
        return Response({
            'success': True,
            'label': _(u"Stop following"),
            'message': message, })
