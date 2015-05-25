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
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('slug', models.SlugField(unique=True, max_length=200, verbose_name='slug')),
                ('description', models.TextField(max_length=10000, verbose_name='description', blank=True)),
                ('latitude', models.FloatField(null=True, verbose_name='latitude', blank=True)),
                ('longitude', models.FloatField(null=True, verbose_name='longitude', blank=True)),
                ('population', models.IntegerField(null=True, verbose_name='population', blank=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('country_code', models.CharField(max_length=10, verbose_name='country code')),
                ('image', models.ImageField(default='img/locations/nowhere.jpg', upload_to=locations.models.get_upload_path, verbose_name='image')),
                ('kind', models.CharField(max_length=10, verbose_name='kind')),
                ('creator', models.ForeignKey(related_name='created_locations', verbose_name='creator', blank=True, to=settings.AUTH_USER_MODEL)),
                ('names', models.ManyToManyField(related_name='alternames', null=True, verbose_name='alternate names', to='locations.AlterLocationName', blank=True)),
                ('parent', models.ForeignKey(verbose_name='parent', blank=True, to='locations.Location', null=True)),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='users', blank=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'location',
                'verbose_name_plural': 'locations',
            },
            bases=(models.Model, locations.models.BackgroundModelMixin),
        ),
        migrations.AddField(
            model_name='country',
            name='location',
            field=models.OneToOneField(related_name='country', to='locations.Location'),
            preserve_default=True,
        ),
    ]
