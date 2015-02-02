# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdminCode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('name_std', models.CharField(max_length=200)),
                ('country', models.CharField(max_length=3)),
                ('code', models.CharField(max_length=10)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AltName',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('geonameid', models.IntegerField()),
                ('iso_code', models.CharField(max_length=7)),
                ('altername', models.CharField(max_length=2000)),
                ('language', models.CharField(max_length=10)),
                ('is_preferred', models.BooleanField(default=False)),
                ('is_short', models.BooleanField(default=False)),
                ('is_colloquial', models.BooleanField(default=False)),
                ('is_historic', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CountryInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('iso_alpha2', models.CharField(max_length=2)),
                ('iso_alpha3', models.CharField(max_length=3)),
                ('iso_numeric', models.IntegerField()),
                ('code', models.CharField(max_length=3)),
                ('name', models.CharField(max_length=200)),
                ('capital', models.CharField(max_length=200)),
                ('area', models.IntegerField(default=0, null=True, blank=True)),
                ('population', models.IntegerField(default=0, null=True, blank=True)),
                ('continent', models.CharField(max_length=2)),
                ('languages', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GeoName',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('name_std', models.CharField(max_length=200)),
                ('latitude', models.FloatField(null=True, blank=True)),
                ('longitude', models.FloatField(null=True, blank=True)),
                ('feature_class', models.CharField(max_length=200)),
                ('feature_code', models.CharField(max_length=200)),
                ('country', models.CharField(max_length=200)),
                ('admin1', models.CharField(max_length=200, null=True, blank=True)),
                ('admin2', models.CharField(max_length=200, null=True, blank=True)),
                ('admin3', models.CharField(max_length=200, null=True, blank=True)),
                ('admin4', models.CharField(max_length=200, null=True, blank=True)),
                ('population', models.IntegerField(default=0, null=True, blank=True)),
                ('elevation', models.IntegerField(default=0, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
