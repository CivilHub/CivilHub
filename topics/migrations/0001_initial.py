# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import mptt.fields
from django.conf import settings
import places_core.models
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('locations', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('name_en', models.CharField(max_length=64, null=True)),
                ('name_pl', models.CharField(max_length=64, null=True)),
                ('name_es', models.CharField(max_length=64, null=True)),
                ('name_de', models.CharField(max_length=64, null=True)),
                ('name_pt', models.CharField(max_length=64, null=True)),
                ('name_fr', models.CharField(max_length=64, null=True)),
                ('name_it', models.CharField(max_length=64, null=True)),
                ('name_cz', models.CharField(max_length=64, null=True)),
                ('description', models.TextField(default='', null=True, blank=True)),
                ('description_en', models.TextField(default='', null=True, blank=True)),
                ('description_pl', models.TextField(default='', null=True, blank=True)),
                ('description_es', models.TextField(default='', null=True, blank=True)),
                ('description_de', models.TextField(default='', null=True, blank=True)),
                ('description_pt', models.TextField(default='', null=True, blank=True)),
                ('description_fr', models.TextField(default='', null=True, blank=True)),
                ('description_it', models.TextField(default='', null=True, blank=True)),
                ('description_cz', models.TextField(default='', null=True, blank=True)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Discussion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(default=b'img/item.png', upload_to=places_core.models.get_image_upload_path, verbose_name='image', blank=True)),
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
                'ordering': ['question'],
                'verbose_name': 'discussion',
                'verbose_name_plural': 'discussions',
            },
            bases=(models.Model,),
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
