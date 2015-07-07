# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0005_auto_20150707_1131'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageLicense',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=128, verbose_name='name')),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
