# -*- coding: utf-8 -*-
from django.db import models


class SimplePollResultsManager(models.Manager):
    """ Custom manager to get results of simple polls.
    """
    def user_results(self, instance, user):
        qs = super(SimplePollResultsManager, self).get_queryset()
        return qs.filter(user=user, poll=instance)

    def poll_results(self, instance):
        qs = super(SimplePollResultsManager, self).get_queryset()
        return qs.filter(poll=instance)
