# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('user_tracker', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='visitor',
            options={'ordering': ('-last_update',), 'verbose_name': 'visitor', 'verbose_name_plural': 'visitors'},
        ),
        migrations.AlterField(
            model_name='visitor',
            name='ip_address',
            field=models.CharField(max_length=20, verbose_name='IP address'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='visitor',
            name='last_update',
            field=models.DateTimeField(verbose_name='last update'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='visitor',
            name='page_views',
            field=models.PositiveIntegerField(default=0, verbose_name='page views'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='visitor',
            name='referrer',
            field=models.CharField(max_length=255, verbose_name='referrer'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='visitor',
            name='session_key',
            field=models.CharField(max_length=40, verbose_name='session key'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='visitor',
            name='session_start',
            field=models.DateTimeField(verbose_name='session start'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='visitor',
            name='url',
            field=models.CharField(max_length=255, verbose_name='url'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='visitor',
            name='user',
            field=models.ForeignKey(verbose_name='user', to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='visitor',
            name='user_agent',
            field=models.CharField(max_length=255, verbose_name='use agent'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='visitor',
            unique_together=set([]),
        ),
    ]
