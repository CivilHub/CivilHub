# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hitcounter', '0002_auto_20150414_0851'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='visit',
            options={'verbose_name': 'visit counter', 'verbose_name_plural': 'visit counters'},
        ),
        migrations.AlterUniqueTogether(
            name='visit',
            unique_together=set([('ip', 'content_type', 'object_id')]),
        ),
    ]
