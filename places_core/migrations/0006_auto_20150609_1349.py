# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('places_core', '0005_auto_20150513_1213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='abusereport',
            name='comment',
            field=models.CharField(default='', max_length=2048, verbose_name='comment', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='abusereport',
            name='reason',
            field=models.PositiveIntegerField(default=12, verbose_name='reason', choices=[(1, 'Pornography'), (2, 'Violence/indicent content'), (3, 'Insults/spread of hatred'), (4, 'Dangerious activities'), (5, 'Usage of children'), (6, 'Spam or other misleading content'), (7, 'Violence of my copyrights'), (8, 'Violence of my privacy'), (9, 'Other legal claims'), (10, 'Duplicate'), (11, 'False information'), (12, 'Is not suitable')]),
            preserve_default=True,
        ),
    ]
