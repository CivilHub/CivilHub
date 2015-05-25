# -*- coding: utf-8 -*-
import json

from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django.db.models import Q
from django.http import Http404
from django.utils.translation import ugettext as _

from actstream.actions import follow, unfollow
from actstream.models import Action, following, actor_stream, target_stream
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from places_core.helpers import get_time_difference

from .serializers import ActionSerializer


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
        instance_name = self.instance._meta.verbose_name.lower()

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
