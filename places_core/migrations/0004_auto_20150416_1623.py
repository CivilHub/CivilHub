# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('places_core', '0003_auto_20150416_1517'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abusereport',
            name='comment',
            field=models.CharField(default='', max_length=2048, blank=True),
            preserve_default=True,
        ),
    ]
