# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

from actstream import action
from actstream.actions import follow, unfollow
from actstream.models import following


def joined_ngo_action(user, ngo):
    """
    Pass django.contrib.auth.User instance along with organization instance to
    send action when user joined to organization.
    """
    if user.is_anonymous():
        return False
    action.send(user, verb=_(u"joined"), target=ngo)
