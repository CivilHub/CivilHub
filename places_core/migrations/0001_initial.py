# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('sites', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AbuseReport',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_pk', models.TextField(verbose_name='object ID')),
                ('comment', models.CharField(max_length=2048)),
                ('status', models.BooleanField(default=False)),
                ('date_reported', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('content_type', models.ForeignKey(related_name='content_type_set_for_abusereport', verbose_name='content type', to='contenttypes.ContentType')),
                ('sender', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('site', models.ForeignKey(to='sites.Site')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
