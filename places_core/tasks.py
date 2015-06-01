# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os
import datetime
import subprocess

from celery import task
from celery.task.base import periodic_task

from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone, translation

from activities.models import user_email_stream
from userspace.models import RegisterDemand
from civmail.messages import *

import logging
logger = logging.getLogger('tasks')


@task(name='tasks.test_schedule')
def test_schedule():
    f = open(LOG, 'a')
    f.write("Test task finished\n")
    f.close()
    logging.info("Test task finished")


@task(name='tasks.send_test_email')
def send_test_email(receiver, subject, title, msg):
    """ Send test email to check if celery beat works. """
    email = TestTemplateEmail()
    return email.send(receiver, {
        'subject': subject,
        'title': title,
        'msg': msg,
    })


@periodic_task(run_every=datetime.timedelta(days=1))
def send_poll_emails():
    """ Send emails with invitations to polls for new users. """
    logger.info(u"[{}]: Started poll emails".format(timezone.now()))
    link = "some-dummy-link"
    name = "This will be link to service poll..."
    min_time = timezone.now() - datetime.timedelta(days=1)
    users = User.objects.filter(
        date_joined__gt=min_time,
        date_joined__lte=timezone.now()
    )
    for user in users:
        logger.info(u"Sending message to user {}".format(user.email))
        email = ServicePollMail()
        email.send(user.email, {'link': link, 'name': name})
    logger.info(u"[{}]: Finished poll emails".format(timezone.now()))


@periodic_task(run_every=datetime.timedelta(hours=12))
def cleanup_register_demands(forced=False):
    """
    Run this task once a day to find not finished registrations and delete
    register demand objects along with user objects created during process.
    """
    logger.info(u"[{}]: Started register cleanup".format(timezone.now()))
    now = timezone.now()
    for demand in RegisterDemand.objects.all():
        delta_t = now - demand.date
        if delta_t > datetime.timedelta(days=1) or forced:
            logger.info(u"Deleting user {} and register demand {}"\
                .format(demand.user.email, demand.pk))
            demand.user.delete()
            demand.delete()
    logger.info(u"[{}]: Finished register cleanup".format(timezone.now()))


@periodic_task(run_every=datetime.timedelta(minutes=5))
def update_indexes():
    """ Update haystack indexes. """
    logger.info(u"[{}]: Started update indexes".format(timezone.now()))
    filename = os.path.join(settings.BASE_DIR, 'manage.py')
    logger.info(u"[{}]: Finished update indexes".format(timezone.now()))
    return subprocess.call(['python', filename, 'update_index'])
