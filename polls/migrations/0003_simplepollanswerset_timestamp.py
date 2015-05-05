# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_auto_20150504_1319'),
    ]

    operations = [
        migrations.AddField(
            model_name='simplepollanswerset',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2015, 5, 4, 11, 29, 27, 851514, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
    ]
