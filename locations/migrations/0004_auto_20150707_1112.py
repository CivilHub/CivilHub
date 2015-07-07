# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def create_default_background_file(apps, schema_editor):
    LocationBackgroundFile = apps.get_model("locations", "LocationBackgroundFile")
    background = LocationBackgroundFile.objects.create(name='default')


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0003_auto_20150707_1108'),
    ]

    operations = [
        migrations.RunPython(create_default_background_file)
    ]
