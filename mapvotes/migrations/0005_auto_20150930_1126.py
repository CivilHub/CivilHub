# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mapvotes', '0004_auto_20150930_0956'),
    ]

    operations = [
        migrations.AddField(
            model_name='marker',
            name='description',
            field=models.TextField(default='', max_length=2000, verbose_name='description', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='marker',
            name='label',
            field=models.CharField(default='', max_length=64, verbose_name='label'),
            preserve_default=True,
        ),
    ]
