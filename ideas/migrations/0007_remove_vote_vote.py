# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ideas', '0006_auto_20150609_1350'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vote',
            name='vote',
        ),
    ]
