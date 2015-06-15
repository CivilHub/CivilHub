# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hitcounter', '0003_auto_20150414_0855'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='visit',
            unique_together=set([]),
        ),
    ]
