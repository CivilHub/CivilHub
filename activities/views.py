# -*- coding: utf-8 -*-
from django.contrib.contenttypes.models import ContentType
from actstream.models import Action, actor_stream, target_stream, user_stream
from rest_framework import viewsets

from .serializers import ActionSerializer


class ActivityViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Entry point for activity API. We can fetch actions for specific user or
    related to specific target. Returned queryset is based on 3 parameters:<br>
        `type` - "actor", "target" or "user"<br>
        `ct`   - Content Type ID for object in question<br>
        `pk`   - ID of selected object
    """
    model = Action
    serializer_class = ActionSerializer
    paginate_by = 15
    request_object = None

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
            return actor_stream(self.request_object)
        elif stream_type == 'target':
            return target_stream(self.request_object)
        else:
            return user_stream(self.request_object)
