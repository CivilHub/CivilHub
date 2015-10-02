# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='description_cz',
        ),
        migrations.RemoveField(
            model_name='category',
            name='description_it',
        ),
        migrations.RemoveField(
            model_name='category',
            name='name_cz',
        ),
        migrations.RemoveField(
            model_name='category',
            name='name_it',
        ),
    ]
