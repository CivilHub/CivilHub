# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def set_location_background_images(apps, schema_editor):
    Location = apps.get_model("locations", "Location")
    LocationBackgroundFile = apps.get_model("locations", "LocationBackgroundFile")
    for l in Location.objects.all():
        if 'nowhere' in l.image.name:
            background = LocationBackgroundFile.objects.get(name='default')
        else:
            background = LocationBackgroundFile.objects.create(
                                            image=l.image.name)
        l.background = background
        l.save()


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0004_auto_20150707_1112'),
    ]

    operations = [
        migrations.RunPython(set_location_background_images)
    ]
