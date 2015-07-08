# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import locations.models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0002_auto_20150424_1157'),
    ]

    operations = [
        migrations.CreateModel(
            name='LocationBackgroundFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(default='img/locations/nowhere.jpg', upload_to=locations.models.get_upload_path, verbose_name='image')),
                ('license', models.PositiveIntegerField(default=1, choices=[(1, 'Creative Commons')])),
                ('author', models.CharField(max_length=128, null=True, verbose_name='author', blank=True)),
                ('source_url', models.URLField(null=True, verbose_name='source url', blank=True)),
                ('name', models.CharField(max_length=128, null=True, verbose_name='name', blank=True)),
                ('description', models.TextField(null=True, verbose_name='description', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='location',
            name='background',
            field=models.ForeignKey(verbose_name='background', blank=True, to='locations.LocationBackgroundFile', null=True),
            preserve_default=True,
        ),
    ]
