# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20150609_1349'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='news',
            options={'ordering': ['title'], 'verbose_name': 'news', 'verbose_name_plural': 'news'},
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
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(max_length=255),
            preserve_default=True,
        ),
    ]
