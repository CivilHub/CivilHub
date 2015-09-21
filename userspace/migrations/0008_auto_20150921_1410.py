# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userspace', '0007_auto_20150706_1046'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='clean_username',
            field=models.SlugField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
    ]
