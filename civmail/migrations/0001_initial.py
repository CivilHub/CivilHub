# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MassEmail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subject', models.CharField(default='', max_length=64, verbose_name='subject')),
                ('body', models.TextField(default='', verbose_name='message')),
                ('status', models.PositiveIntegerField(default=1, verbose_name='status', choices=[(1, 'pending'), (2, 'sent')])),
                ('sent_at', models.DateTimeField(null=True, verbose_name='date sent', blank=True)),
            ],
            options={
                'verbose_name': 'mass email',
                'verbose_name_plural': 'mass emails',
            },
            bases=(models.Model,),
        ),
    ]
