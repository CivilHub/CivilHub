# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import locations.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AlterLocationName',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('altername', models.CharField(max_length=200)),
                ('language', models.CharField(max_length=2)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(max_length=2)),
            ],
            options={
                'ordering': ['code'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('slug', models.SlugField(unique=True, max_length=200)),
                ('description', models.TextField(max_length=10000, blank=True)),
                ('latitude', models.FloatField(null=True, blank=True)),
                ('longitude', models.FloatField(null=True, blank=True)),
                ('population', models.IntegerField(null=True, blank=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('country_code', models.CharField(max_length=10)),
                ('image', models.ImageField(default='img/locations/nowhere.jpg', upload_to=locations.models.get_upload_path)),
                ('kind', models.CharField(max_length=10)),
                ('creator', models.ForeignKey(related_name='created_locations', blank=True, to=settings.AUTH_USER_MODEL)),
                ('names', models.ManyToManyField(related_name='alternames', null=True, to='locations.AlterLocationName', blank=True)),
                ('parent', models.ForeignKey(blank=True, to='locations.Location', null=True)),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='country',
            name='location',
            field=models.OneToOneField(related_name='country', to='locations.Location'),
            preserve_default=True,
        ),
    ]
