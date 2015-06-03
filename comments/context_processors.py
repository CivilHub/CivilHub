# -*- coding: utf-8 -*-
import json

from django.contrib.contenttypes.models import ContentType

from .models import CustomComment


def ctmap(request):
    """ Returns different content type id's required for generic relations.
    """
    ct = ContentType.objects.get_for_model(CustomComment).pk
    return {'CT_MAP': json.dumps({
        'comments_customcomment': ct, }), }
