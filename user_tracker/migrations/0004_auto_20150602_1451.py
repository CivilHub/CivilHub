# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_tracker', '0003_visitor_checked'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitor',
            name='user_agent',
            field=models.CharField(max_length=255, verbose_name='user agent'),
            preserve_default=True,
        ),
    ]
