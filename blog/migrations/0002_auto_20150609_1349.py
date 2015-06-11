# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='content',
            field=models.TextField(max_length=10248, null=True, verbose_name='content', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='news',
            name='title',
            field=models.CharField(max_length=64, verbose_name='title'),
            preserve_default=True,
        ),
    ]
