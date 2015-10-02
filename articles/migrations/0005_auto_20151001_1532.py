# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0004_auto_20150319_1520'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='content_cz',
        ),
        migrations.RemoveField(
            model_name='article',
            name='content_it',
        ),
        migrations.RemoveField(
            model_name='article',
            name='subtitle_cz',
        ),
        migrations.RemoveField(
            model_name='article',
            name='subtitle_it',
        ),
        migrations.RemoveField(
            model_name='article',
            name='title_cz',
        ),
        migrations.RemoveField(
            model_name='article',
            name='title_it',
        ),
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
