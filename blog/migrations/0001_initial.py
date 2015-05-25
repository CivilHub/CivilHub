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
                ('slug', models.SlugField(max_length=64)),
                ('description', models.TextField(default='', max_length=1024, null=True, blank=True)),
                ('description_en', models.TextField(default='', max_length=1024, null=True, blank=True)),
                ('description_pl', models.TextField(default='', max_length=1024, null=True, blank=True)),
                ('description_es', models.TextField(default='', max_length=1024, null=True, blank=True)),
                ('description_de', models.TextField(default='', max_length=1024, null=True, blank=True)),
                ('description_pt', models.TextField(default='', max_length=1024, null=True, blank=True)),
                ('description_fr', models.TextField(default='', max_length=1024, null=True, blank=True)),
                ('description_it', models.TextField(default='', max_length=1024, null=True, blank=True)),
                ('description_cz', models.TextField(default='', max_length=1024, null=True, blank=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(default=b'img/item.png', upload_to=places_core.models.get_image_upload_path, verbose_name='image', blank=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_edited', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=64)),
                ('slug', models.SlugField(unique=True, max_length=64)),
                ('content', models.TextField(max_length=10248, null=True, blank=True)),
                ('edited', models.BooleanField(default=False)),
                ('category', models.ForeignKey(verbose_name='category', blank=True, to='blog.Category', null=True)),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('location', models.ForeignKey(to='locations.Location')),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags')),
            ],
            options={
                'ordering': ['title'],
                'verbose_name': 'news',
                'verbose_name_plural': 'newses',
            },
            bases=(models.Model,),
        ),
    ]
