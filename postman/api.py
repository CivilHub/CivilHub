"""
This module provides an API to the django-postman application,
for an easy usage from other applications in the project.

Sample:
Suppose an application managing Event objects. Whenever a new Event is generated,
you want to broadcast an announcement to Users who have subscribed
to be informed of the availability of such a kind of Event.

from postman.api import pm_broadcast
events = Event.objects.filter(...)
for e in events:
    pm_broadcast(
        sender=e.author,
        recipients=e.subscribers,
        subject='New {0} at Our School: {1}'.format(e.type, e.title),
        body=e.description)
"""
from __future__ import unicode_literals

from django.contrib.sites.models import Site
try:
    from django.utils.timezone import now  # Django 1.4 aware datetimes
except ImportError:
    from datetime import datetime
    now = datetime.now

from postman.models import Message, STATUS_PENDING, STATUS_ACCEPTED


def _get_site():
    # do not require the sites framework to be installed ; and no request object is available here
    return Site.objects.get_current() if Site._meta.installed else None


def pm_broadcast(sender, recipients, subject, body='', skip_notification=False):
    """
    Broadcast a message to multiple Users.
    For an easier cleanup, all these messages are directly marked as archived
    and deleted on the sender side.
    The message is expected to be issued from a trusted application, so moderation
    is not necessary and the status is automatically set to 'accepted'.

    Optional argument:
        ``skip_notification``: if the normal notification event is not wished
    """
    message = Message(subject=subject, body=body, sender=sender,
        sender_archived=True, sender_deleted_at=now(),
        moderation_status=STATUS_ACCEPTED, moderation_date=now())
    if not isinstance(recipients, (tuple, list)):
        recipients = (recipients,)
    for recipient in recipients:
        message.recipient = recipient
        message.pk = None
        message.save()
        if not skip_notification:
            message.notify_users(STATUS_PENDING, _get_site())


def pm_write(sender, recipient, subject, body='', skip_notification=False,
        auto_archive=False, auto_delete=False, auto_moderators=None):
    """
    Write a message to a User.
    Contrary to pm_broadcast(), the message is archived and/or deleted on
    the sender side only if requested.
    The message may come from an untrusted application, a gateway for example,
    so it may be useful to involve some auto moderators in the processing.

    Optional arguments:
        ``skip_notification``: if the normal notification event is not wished
        ``auto_archive``: to mark the message as archived on the sender side
        ``auto_delete``: to mark the message as deleted on the sender side
        ``auto_moderators``: a list of auto-moderation functions
    """
    message = Message(subject=subject, body=body, sender=sender, recipient=recipient)
    initial_status = message.moderation_status
    if auto_moderators:
        message.auto_moderate(auto_moderators)
    else:
        message.moderation_status = STATUS_ACCEPTED
    message.clean_moderation(initial_status)
    if auto_archive:
        message.sender_archived = True
    if auto_delete:
        message.sender_deleted_at = now()
    message.save()
    if not skip_notification:
        message.notify_users(initial_status, _get_site())
