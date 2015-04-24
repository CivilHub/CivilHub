# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='children_list',
            field=models.CharField(help_text="List of children ID's separated with comma", max_length=255, null=True, verbose_name='children list', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='location',
            name='parent_list',
            field=models.CharField(help_text="List of parent location ID's separated with comma", max_length=255, null=True, verbose_name='parent list', blank=True),
            preserve_default=True,
        ),
    ]
