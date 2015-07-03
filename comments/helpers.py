# -*- coding: utf-8 -*-
import re

from django.contrib.auth.models import User
from django.utils.translation import ugettext as _

from civmail.messages import CommentNotify
from notifications.models import notify

from .config import get_config


# A little hack for gettext because verbs are stored as-is in database
NOTIFY_VERB = u"mentioned you in his comment"
translated = _(NOTIFY_VERB)
classname = "mention user-window-toggle"
userreg = re.compile(r'\[~(?P<username>[\w\d]+)*\]')
link_tpl = '@<a class="{}" href="{}" data-target="{}" data-username="{}">{}</a>'


def notify_author(obj):
    message = CommentNotify()
    message_context = {
        'lang': obj.user.profile.lang,
        'url': obj.get_absolute_url(),
        'reason': obj.get_reason_display(), }
    if get_config('NOTIFY_EMAIL'):
        message.send(obj.user.email, message_context)


def mention_notify(comment):
    """ Notify mentioned users when comment is created.
    """
    for match in userreg.finditer(comment.comment):
        try:
            user = User.objects.get(username=match.groups()[0])
        except User.DoesNotExist:
            user = None
        if user is not None and user != comment.user:
            notify(comment.user, user,
                key="customcomment",
                verb=NOTIFY_VERB,
                action_target=comment)


def parse_mentions(comment):
    """ Find user mentions and return formatted HTML for display.
    """
    for match in userreg.finditer(comment):
        user = User.objects.get(username=match.groups()[0])
        html = link_tpl.format(classname, user.profile.get_absolute_url(),
            user.pk, user.username, user.get_full_name())
        comment = comment.replace(match.group(), html)
    return comment
