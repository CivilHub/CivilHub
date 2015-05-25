# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_auto_20150316_1833'),
    ]

    operations = [
        migrations.AddField(
            model_name='socialforumentry',
            name='is_edited',
            field=models.BooleanField(default=False, verbose_name='edited'),
            preserve_default=True,
        ),
    ]
