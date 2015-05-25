# -*- coding: utf-8 -*-
import datetime

from django.utils import timezone

from actstream.models import Action


def user_email_stream(user):
    """ Used in stream email message.
    """
    time_diff = timezone.now() - datetime.timedelta(days=7)
    return Action.objects.mystream(user).filter(timestamp__gt=time_diff)
