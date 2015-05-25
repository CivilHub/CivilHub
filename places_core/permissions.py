# -*- coding: utf-8 -*-

# Custom user permissions. If such a need arises, we will use
# some package such a django-guardian.
from django.contrib.auth.models import User, Group
from userspace.models import UserProfile


def is_moderator(user, location):
    """
    This function check whether the user is a mod of
    a given location. Returns 'True' also for superadmins
    and 'supermoderators'.
    """
    if user.is_superuser:
        return True

    # The group name is written "non-dynamically" !!!
    if 'Editor' in [x.name for x in Group.objects.all()]:
        return True

    if user.is_anonymous():
        return False

    profile = UserProfile.objects.get(user = user)
    if profile.mod_areas.filter(pk=location.pk).exists():
        return True

    return False
