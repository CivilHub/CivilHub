# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('description', models.TextField(default='', blank=True)),
            ],
            options={
                'verbose_name': 'blog category',
                'verbose_name_plural': 'blog categories',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='BlogEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('slug', models.CharField(max_length=210, verbose_name='slug')),
                ('content', models.TextField(default='', verbose_name='content')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('date_edited', models.DateTimeField(auto_now=True, verbose_name='date edited')),
                ('tags', models.CharField(default='', help_text='List of tags separated by comma', max_length=255, verbose_name='tags', blank=True)),
                ('object_id', models.PositiveIntegerField(null=True, blank=True)),
                ('author', models.ForeignKey(related_name='simpleblog_entries', verbose_name='author', to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(verbose_name='category', blank=True, to='simpleblog.BlogCategory', null=True)),
                ('content_type', models.ForeignKey(blank=True, to='contenttypes.ContentType', null=True)),
            ],
            options={
                'verbose_name': 'blog entry',
                'verbose_name_plural': 'blog entries',
            },
            bases=(models.Model,),
        ),
    ]
