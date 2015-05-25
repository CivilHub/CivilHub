# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_tracker', '0002_auto_20150522_1413'),
    ]

    operations = [
        migrations.AddField(
            model_name='visitor',
            name='checked',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
