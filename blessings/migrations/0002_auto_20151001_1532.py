# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blessings', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blessing',
            options={'ordering': ('-date',), 'verbose_name': 'recommendation', 'verbose_name_plural': 'recommendations'},
        ),
    ]
