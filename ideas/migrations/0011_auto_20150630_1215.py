# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ideas', '0010_remove_vote_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='negative_comment',
            field=models.TextField(null=True, verbose_name='comment', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='vote',
            name='positive_comment',
            field=models.TextField(null=True, verbose_name='comment', blank=True),
            preserve_default=True,
        ),
    ]
