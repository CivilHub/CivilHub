# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ideas', '0004_auto_20150601_1323'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='status',
            field=models.PositiveIntegerField(default=2, choices=[(1, 'positive'), (2, 'negative'), (3, 'revoked')]),
            preserve_default=True,
        ),
    ]
