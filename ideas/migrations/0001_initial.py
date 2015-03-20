# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
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
                ('description', models.TextField(max_length=1024)),
                ('description_en', models.TextField(max_length=1024, null=True)),
                ('description_pl', models.TextField(max_length=1024, null=True)),
                ('description_es', models.TextField(max_length=1024, null=True)),
                ('description_de', models.TextField(max_length=1024, null=True)),
                ('description_pt', models.TextField(max_length=1024, null=True)),
                ('description_fr', models.TextField(max_length=1024, null=True)),
                ('description_it', models.TextField(max_length=1024, null=True)),
                ('description_cz', models.TextField(max_length=1024, null=True)),
            ],
            options={
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Idea',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(default=b'img/item.png', upload_to=places_core.models.get_image_upload_path, verbose_name='image', blank=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_edited', models.DateTimeField(auto_now=True, null=True)),
                ('name', models.CharField(max_length=64)),
                ('slug', models.SlugField(unique=True, max_length=70)),
                ('description', models.TextField(default='', blank=True)),
                ('status', models.BooleanField(default=True)),
                ('edited', models.BooleanField(default=False)),
                ('category', models.ForeignKey(blank=True, to='ideas.Category', null=True)),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('location', models.ForeignKey(to='locations.Location')),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags')),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'idea',
                'verbose_name_plural': 'ideas',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('vote', models.BooleanField(default=False)),
                ('date_voted', models.DateTimeField(auto_now=True)),
                ('idea', models.ForeignKey(to='ideas.Idea')),
                ('user', models.ForeignKey(related_name='idea_votes', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'vote',
                'verbose_name_plural': 'votes',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together=set([('user', 'idea')]),
        ),
    ]
