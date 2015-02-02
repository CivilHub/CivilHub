# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0001_initial'),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MapPointer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_pk', models.TextField(verbose_name='object ID')),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('content_type', models.ForeignKey(related_name='content_type_set_for_mappointer', verbose_name='content type', to='contenttypes.ContentType')),
                ('location', models.ForeignKey(blank=True, to='locations.Location', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
