# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hitcounter', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visit',
            name='visit_count',
            field=models.IntegerField(default=1),
            preserve_default=True,
        ),
    ]
