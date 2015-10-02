# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mapvotes', '0005_auto_20150930_1126'),
    ]

    operations = [
        migrations.AlterField(
            model_name='marker',
            name='voting',
            field=models.ForeignKey(related_name='markers', verbose_name='voting', to='mapvotes.Voting'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='voting',
            name='is_limited',
            field=models.BooleanField(default=False, help_text='Limit user votes to just one marker in set', verbose_name='limited'),
            preserve_default=True,
        ),
    ]
