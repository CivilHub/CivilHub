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
                ('slug', models.SlugField(max_length=64)),
                ('description', models.TextField(default='', max_length=1024, null=True, blank=True)),
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
                ('imagableitemmixin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='places_core.ImagableItemMixin')),
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
            bases=('places_core.imagableitemmixin', models.Model),
        ),
    ]
