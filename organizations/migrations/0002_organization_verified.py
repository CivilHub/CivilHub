# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='verified',
            field=models.BooleanField(default=False, verbose_name='is verified'),
            preserve_default=True,
        ),
    ]
