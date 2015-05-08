# -*- coding: utf-8 -*-
from collections import defaultdict

from django.contrib.contenttypes.models import ContentType
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
            q = q | Q(actor_content_type=content_type_id,
                      actor_object_id__in=object_ids, ) | Q(
                          target_content_type=content_type_id,
                          target_object_id__in=object_ids, ) | Q(
                              action_object_content_type=content_type_id,
                              action_object_object_id__in=object_ids, )

        return self.filter(q, **kwargs)

    @stream
    def ngostream(self, obj, **kwargs):
        """
        Activity stream for NGO, presents actions of all memebers.
        """
        q = Q()
        check(obj)

        if not hasattr(obj, 'users'):
            return self.none()

        self_type = ContentType.objects.get_for_model(obj)
        user_type = ContentType.objects.get(app_label="auth", model="user")
        user_list = [int(x.pk) for x in obj.users.all()]

        q = q | Q(target_content_type=self_type, target_object_id=obj.pk)

        q = q | Q(actor_content_type=user_type, actor_object_id__in=user_list)

        return self.filter(q, **kwargs)

    @stream
    def location(self, obj, **kwargs):
        """
        Actstream for location - we try to include also actions related to
        different content types published in this location, eg. comments
        and votes.
        """
        q = Q()
        check(obj)

        if not hasattr(obj, 'published_items'):
            return self.none()

        self_type = ContentType.objects.get_for_model(obj)
        id_list = [obj.pk, ] + [x[0] for x in obj.location_set.values_list('pk')]
        q = q | Q(target_content_type=self_type, target_object_id__in=id_list)

        for ct, id_list in obj.published_items().iteritems():
            q = q | Q(target_content_type=ct, target_object_id__in=id_list)

        return self.filter(q, **kwargs)
