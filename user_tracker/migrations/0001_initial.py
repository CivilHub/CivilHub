# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Visitor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('session_key', models.CharField(max_length=40)),
                ('ip_address', models.CharField(max_length=20)),
                ('user_agent', models.CharField(max_length=255)),
                ('referrer', models.CharField(max_length=255)),
                ('url', models.CharField(max_length=255)),
                ('page_views', models.PositiveIntegerField(default=0)),
                ('session_start', models.DateTimeField()),
                ('last_update', models.DateTimeField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('-last_update',),
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='visitor',
            unique_together=set([('session_key', 'ip_address')]),
        ),
    ]
