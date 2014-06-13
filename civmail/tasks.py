# -*- coding: utf-8 -*-
from __future__ import absolute_import
from celery import task
from django.contrib.auth.models import User
from django.utils import translation
from actstream.models import user_stream
from .messages import *


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


@task(name='tasks.send_test_email')
def send_test_email(receiver, subject, title, msg):
    """ Send test email to check if celery beat works. """
    email = TestTemplateEmail()
    return email.send(receiver, {
        'subject': subject,
        'title': title,
        'msg': msg,
    })
