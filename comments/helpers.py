# -*- coding: utf-8 -*-
from civmail.messages import CommentNotify

from .config import get_config


def notify_author(obj):
    message = CommentNotify()
    message_context = {
        'lang': obj.user.profile.lang,
        'url': obj.get_absolute_url(),
        'reason': obj.get_reason_display(), }
    if get_config('NOTIFY_EMAIL'):
        message.send(obj.user.email, message_context)
