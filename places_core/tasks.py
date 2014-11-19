# -*- coding: utf-8 -*-
"""
This file contains all tasks for Celery task manager. They should be in
separate package-related files, but this leads to many import errors.
"""
from __future__ import absolute_import
from celery import task
from datetime import timedelta
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone, translation
from actstream.models import user_stream
from userspace.models import RegisterDemand
from civmail.messages import *

import os, logging
LOG = os.path.join(settings.BASE_DIR, 'logs/django.log')
logging.basicConfig(filename = LOG, level = logging.INFO)


#
# Test tasks
# ----------
#
@task(name='tasks.test_schedule')
def test_schedule():
    f = open(LOG, 'a')
    f.write("Test task finished\n")
    f.close()
    logging.info("Test task finished")


#
# Email tasks
# -----------
#
@task(name='tasks.send_notification_emails')
def notification_emails():
    """
    Send activity stream emails.
    """
    users = User.objects.all()
    for user in users:
        stream = user_stream(user)
        email = UserStreamMail()
        translation.activate(user.profile.lang)
        return email.send(user.email, {'stream': stream})


@task(name='tasks.send_poll_email')
def send_poll_email(user_pk):
    """
    Send email with invitation to poll for every new registered user some
    time after registeration.
    
    TODO: trzeba pozmieniać dummy-linki i utworzyć faktyczną stronę ankiety.
    """
    user = User.objects.get(pk=user_pk)
    translation.activate(user.profile.lang)
    email = ServicePollMail()
    return email.send(user.email, {
        'link': 'some-dummy-link',
        'name': 'This will be link to service poll...',
    })


@task(name='tasks.send_test_email')
def send_test_email(receiver, subject, title, msg):
    """ Send test email to check if celery beat works. """
    email = TestTemplateEmail()
    return email.send(receiver, {
        'subject': subject,
        'title': title,
        'msg': msg,
    })


#
# Userspace tasks
# ---------------
#
@task(name='tasks.cleanup_register_demands')
def cleanup_register_demands(forced=False):
    """
    Run this task once a day to find not finished registrations and delete
    register demand objects along with user objects created during process.
    """
    now = timezone.now()
    for demand in RegisterDemand.objects.all():
        delta_t = now - demand.date
        if delta_t > timedelta(days=1) or forced:
            demand.user.delete()
            demand.delete()
