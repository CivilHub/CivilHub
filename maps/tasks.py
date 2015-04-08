# -*- coding: utf-8 -*-
from __future__ import absolute_import

import datetime

from celery.task.base import periodic_task

from locations.models import Location

from .helpers import create_country_clusters, make_region_cluster


@periodic_task(run_every=datetime.timedelta(minutes=20))
def update_marker_cluster_cache():
    """ Updates all cached map clusters related to locations. """
    create_country_clusters()
    for location in Location.objects.filter(kind__in=['PPLA', 'PPLC',]):
        make_region_cluster(location)
