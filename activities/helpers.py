# -*- coding: utf-8 -*-
from actstream.models import Action, actor_stream, target_stream

from .serializers import ActionSerializer


def get_first_page(obj, stream_type="actor"):
    """ Simplified method to get first activity stream page to display
        it as-is without further API calls from JavaScript. Results are
        serialized in the same way as in regular API view.
    """
    if stream_type == 'actor':
        qs = actor_stream(obj)
    elif stream_type == 'target':
        qs = target_stream(obj)
    elif stream_type == 'ngo':
        qs = Action.objects.ngostream(obj)
    elif stream_type == 'location':
        qs = Action.objects.location(obj)
    else:
        qs = Action.objects.mystream(obj)
    return {
        'results': ActionSerializer(qs[:15], many=True).data,
        'count': len(qs),
        'next': len(qs) > 15, }
