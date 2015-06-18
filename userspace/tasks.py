# -*- coding: utf-8 -*-
from __future__ import absolute_import

import datetime

from celery.task.base import periodic_task

from .models import CloseAccountDemand


@periodic_task(run_every=datetime.timedelta(hours=12))
def clear_accounts():
    """ Check account delete demands and deactivate every account that has
        related delete demand.
    """
    for demand in CloseAccountDemand.filter(date__lte=timezone.now(),
                                            is_deleted=False):
        demand.deactivate()
