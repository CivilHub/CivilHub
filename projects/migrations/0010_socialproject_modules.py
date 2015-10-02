# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0009_attachment_tasks'),
    ]

    operations = [
        migrations.AddField(
            model_name='socialproject',
            name='modules',
            field=models.TextField(default='2,3,4,5', verbose_name='modules'),
            preserve_default=True,
        ),
    ]
