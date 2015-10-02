# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('civmail', '0003_auto_20150504_1928'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='massemail',
            name='body_cz',
        ),
        migrations.RemoveField(
            model_name='massemail',
            name='body_it',
        ),
        migrations.RemoveField(
            model_name='massemail',
            name='subject_cz',
        ),
        migrations.RemoveField(
            model_name='massemail',
            name='subject_it',
        ),
    ]
