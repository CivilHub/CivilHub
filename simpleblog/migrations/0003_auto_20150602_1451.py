# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('simpleblog', '0002_blogentry_image'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blogentry',
            options={'ordering': ['-date_created'], 'verbose_name': 'blog entry', 'verbose_name_plural': 'blog entries'},
        ),
    ]
