# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0004_invitation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invitation',
            name='key',
            field=models.CharField(unique=True, max_length=255, verbose_name='key', blank=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='invitation',
            unique_together=set([('user', 'organization')]),
        ),
    ]
