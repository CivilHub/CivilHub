# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_auto_20150506_0941'),
    ]

    operations = [
        migrations.AddField(
            model_name='attachment',
            name='mime_type',
            field=models.CharField(default='', max_length=255),
            preserve_default=True,
        ),
    ]
