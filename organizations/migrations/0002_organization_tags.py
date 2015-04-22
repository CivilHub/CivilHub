# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='tags',
            field=models.CharField(default='', help_text='Tags separated by comma', max_length=255, verbose_name='tags', blank=True),
            preserve_default=True,
        ),
    ]
