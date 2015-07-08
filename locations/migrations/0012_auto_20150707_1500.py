# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0011_remove_location_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='locationbackgroundfile',
            name='author',
        ),
        migrations.AddField(
            model_name='locationbackgroundfile',
            name='authors',
            field=models.CharField(max_length=255, null=True, verbose_name='authors', blank=True),
            preserve_default=True,
        ),
    ]
