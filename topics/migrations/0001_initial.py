# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields
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
                ('description', models.TextField(default='', null=True, blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Discussion',
            fields=[
                ('imagableitemmixin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='places_core.ImagableItemMixin')),
                ('question', models.CharField(max_length=255)),
                ('slug', models.SlugField(unique=True, max_length=255)),
                ('intro', models.TextField()),
                ('status', models.BooleanField(default=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_edited', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(blank=True, to='topics.Category', null=True)),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('location', models.ForeignKey(to='locations.Location')),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags')),
            ],
            options={
            },
            bases=('places_core.imagableitemmixin', models.Model),
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_edited', models.DateTimeField(auto_now=True)),
                ('is_edited', models.BooleanField(default=False)),
                ('lft', models.PositiveIntegerField(editable=False, db_index=True)),
                ('rght', models.PositiveIntegerField(editable=False, db_index=True)),
                ('tree_id', models.PositiveIntegerField(editable=False, db_index=True)),
                ('level', models.PositiveIntegerField(editable=False, db_index=True)),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('discussion', models.ForeignKey(to='topics.Discussion')),
                ('parent', mptt.fields.TreeForeignKey(related_name='children', blank=True, to='topics.Entry', null=True)),
            ],
            options={
                'ordering': ['-date_created'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EntryVote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vote', models.BooleanField(default=False)),
                ('date_voted', models.DateTimeField(auto_now_add=True)),
                ('entry', models.ForeignKey(related_name='votes', to='topics.Entry')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
