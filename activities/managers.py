# -*- coding: utf-8 -*-
from collections import defaultdict

from django.db.models import Q
from django.db.models import get_model

from actstream.managers import ActionManager, stream
from actstream.registry import check


class CivilActionManager(ActionManager):

    @stream
    def mystream(self, obj, **kwargs):
        """
        Custom stream for users. Includes votes and comments info.
        """
        q = Q()
        check(obj)

        objects_by_content_type = defaultdict(lambda: [])

        following = get_model('actstream', 'follow').objects\
            .filter(user=obj).values_list('content_type_id', 'object_id', )
        for content_type_id, object_id in following.iterator():
            objects_by_content_type[content_type_id].append(object_id)

        for content_type_id, object_ids in objects_by_content_type.items():
            q = q | Q(
                actor_content_type=content_type_id,
                actor_object_id__in=object_ids,
            ) | Q(
                target_content_type=content_type_id,
                target_object_id__in=object_ids,
            ) | Q(
                action_object_content_type=content_type_id,
                action_object_object_id__in=object_ids,
            )

        return self.filter(q, **kwargs)
