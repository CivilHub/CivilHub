# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import organizations.models
import taggit.managers
import locations.models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_socialproject_authors_group'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('locations', '__first__'),
        ('taggit', '0002_auto_20150129_1711'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64, verbose_name='name')),
                ('description', models.TextField(default='', verbose_name='description', blank=True)),
            ],
            options={
                'verbose_name': 'category',
                'verbose_name_plural': 'categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('slug', models.CharField(max_length=210, verbose_name='slug')),
                ('description', models.TextField(default='', verbose_name='description', blank=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('date_modified', models.DateTimeField(auto_now=True, verbose_name='date modified')),
                ('krs', models.CharField(default='', max_length=255, verbose_name='KRS', blank=True)),
                ('email', models.EmailField(max_length=75, null=True, verbose_name='contact mail', blank=True)),
                ('website', models.URLField(null=True, verbose_name='website', blank=True)),
                ('logo', models.ImageField(default='img/ngo/default.jpg', upload_to=organizations.models.logo_upload_path)),
                ('category', models.ForeignKey(verbose_name='category', blank=True, to='organizations.Category', null=True)),
                ('creator', models.ForeignKey(related_name='created_organizations', verbose_name='creator', to=settings.AUTH_USER_MODEL)),
                ('locations', models.ManyToManyField(related_name='organizations', null=True, verbose_name='locations', to='locations.Location', blank=True)),
                ('projects', models.ManyToManyField(related_name='mentors', null=True, to='projects.SocialProject', blank=True)),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags')),
                ('users', models.ManyToManyField(related_name='organizations', null=True, verbose_name='members', to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
                'verbose_name': 'organization',
                'verbose_name_plural': 'organizations',
            },
            bases=(models.Model, locations.models.BackgroundModelMixin),
        ),
    ]
