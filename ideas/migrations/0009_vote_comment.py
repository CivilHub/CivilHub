# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ideas', '0008_auto_20150626_1143'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='comment',
            field=models.TextField(null=True, verbose_name='comment', blank=True),
            preserve_default=True,
        ),
    ]
