# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('places_core', '0007_redirectrule'),
    ]

    operations = [
        migrations.AlterField(
            model_name='redirectrule',
            name='url_in',
            field=models.CharField(max_length=200),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='redirectrule',
            name='url_out',
            field=models.CharField(max_length=200),
            preserve_default=True,
        ),
    ]
