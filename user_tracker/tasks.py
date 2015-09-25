# -*- coding: utf-8 -*-
import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone

from celery.task.base import periodic_task

from civmail.messages import LastLoginNotifyEmail

from .models import Visitor

import logging
logger = logging.getLogger('tracker')


TIME_PERIOD = datetime.timedelta(days=int(getattr(settings, 'TIME_PERIOD', 10)))


@periodic_task(run_every=datetime.timedelta(hours=12))
def login_remind_messages():
    """ Send emails to uses that were not logged in during selected time period.
        This task iterates over Visit objects in database and, if visitor is not
        anonymous and his last entry last_update is older then period, sends him
        an email with invitation to login again.
    """
    min_date = timezone.now() - TIME_PERIOD

    logger.info("Track for users not active since %s" % min_date)

    for user in User.objects.all():

        visit = Visitor.objects.last_for_user(user)

        if visit is None:
            continue

        if visit.last_update < min_date and not visit.checked:

            logger.info("Found user %s" % user.get_full_name())

            #message = LastLoginNotifyEmail()
            #message.send(user.email, {'lang': user.profile.lang, })

            # Update visit to avoid sending message again
            visit.checked = True
            visit.save()

    logger.info("Task finished")
