# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0008_auto_20150707_1335'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='locationbackgroundfile',
            name='license',
        ),
    ]
