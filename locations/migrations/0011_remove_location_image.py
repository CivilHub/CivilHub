# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0010_locationbackgroundfile_license'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='image',
        ),
    ]
