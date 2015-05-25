# -*- coding: utf-8 -*-
import datetime

from django.contrib.auth.models import User
from django.utils import timezone

from celery.task.base import periodic_task

from activities.models import user_email_stream

from .messages import UserStreamMail
from .models import MassEmail


# @periodic_task(run_every=datetime.timedelta(days=7))
# def notification_emails():
#     """ Send activity stream emails.
#     """
#     for user in User.objects.filter(is_staff=False, is_superuser=False):
#         email_context = {
#             'lang': user.profile.lang,
#             'stream': user_email_stream(user),
#         }
#         UserStreamMail().send(user.email, email_context)


# @periodic_task(run_every=datetime.timedelta(minutes=5))
# def mass_mails():
#     """ Send newsletter pending messages.
#     """
#     messages = MassEmail.objects.filter(status=1)\
#         .exclude(scheduled_at__gte=timezone.now())
#     for message in messages:
#         message.send()
