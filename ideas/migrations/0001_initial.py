# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taggit', '0002_auto_20150217_1534'),
        ('places_core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('description', models.TextField(max_length=1024)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Idea',
            fields=[
                ('imagableitemmixin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='places_core.ImagableItemMixin')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_edited', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(max_length=64)),
                ('slug', models.SlugField(unique=True, max_length=64)),
                ('description', models.TextField(max_length=20480, null=True, blank=True)),
                ('status', models.BooleanField(default=True)),
                ('edited', models.BooleanField(default=False)),
                ('category', models.ForeignKey(blank=True, to='ideas.Category', null=True)),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('location', models.ForeignKey(to='locations.Location')),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags')),
            ],
            options={
                'ordering': ['name'],
            },
            bases=('places_core.imagableitemmixin', models.Model),
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vote', models.BooleanField(default=False)),
                ('date_voted', models.DateTimeField(auto_now=True)),
                ('idea', models.ForeignKey(to='ideas.Idea')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
