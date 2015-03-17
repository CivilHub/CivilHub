# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import projects.models
from django.conf import settings
import locations.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('locations', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialForumEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField(default='', verbose_name='content')),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('date_changed', models.DateTimeField(auto_now=True, verbose_name='date edited')),
                ('creator', models.ForeignKey(related_name='social_entries', verbose_name='author', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['date_created'],
                'verbose_name': 'forum entry',
                'verbose_name_plural': 'forum entries',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SocialForumTopic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('slug', models.CharField(max_length=210, verbose_name='slug')),
                ('description', models.TextField(default='', verbose_name='description', blank=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('date_changed', models.DateTimeField(auto_now=True, verbose_name='date edited')),
                ('is_closed', models.BooleanField(default=False, verbose_name='closed')),
                ('creator', models.ForeignKey(related_name='social_topics', verbose_name='creator', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'discussion',
                'verbose_name_plural': 'discussions',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SocialProject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('slug', models.CharField(max_length=210, verbose_name='slug')),
                ('description', models.TextField(default='', verbose_name='description', blank=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('date_changed', models.DateTimeField(auto_now=True, verbose_name='date changed')),
                ('is_done', models.BooleanField(default=False, verbose_name='finished')),
                ('image', models.ImageField(default='img/projects/default.jpg', upload_to=projects.models.get_upload_path, blank=True)),
                ('creator', models.ForeignKey(related_name='projects', verbose_name='created by', to=settings.AUTH_USER_MODEL)),
                ('location', models.ForeignKey(related_name='projects', verbose_name='location', to='locations.Location')),
                ('participants', models.ManyToManyField(to=settings.AUTH_USER_MODEL, null=True, verbose_name='participants', blank=True)),
            ],
            options={
                'verbose_name': 'project',
                'verbose_name_plural': 'projects',
            },
            bases=(locations.models.BackgroundModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(editable=False, db_index=True)),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('description', models.TextField(default='', verbose_name='description', blank=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('date_changed', models.DateTimeField(auto_now=True, verbose_name='date changed')),
                ('date_limited', models.DateTimeField(null=True, verbose_name='time limit', blank=True)),
                ('is_done', models.BooleanField(default=False, verbose_name='finished')),
                ('creator', models.ForeignKey(related_name='tasks', verbose_name='created by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['order'],
                'verbose_name': 'task',
                'verbose_name_plural': 'tasks',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TaskGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(editable=False, db_index=True)),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('description', models.TextField(default='', verbose_name='description', blank=True)),
                ('creator', models.ForeignKey(related_name='task_groups', verbose_name='created by', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(verbose_name='project', to='projects.SocialProject')),
            ],
            options={
                'ordering': ['order'],
                'verbose_name': 'task group',
                'verbose_name_plural': 'task groups',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='task',
            name='group',
            field=models.ForeignKey(verbose_name='group', to='projects.TaskGroup'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='task',
            name='participants',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL, null=True, verbose_name='participants', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='socialforumtopic',
            name='project',
            field=models.ForeignKey(related_name='discussions', verbose_name='project', to='projects.SocialProject'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='socialforumentry',
            name='topic',
            field=models.ForeignKey(verbose_name='discussion', to='projects.SocialForumTopic'),
            preserve_default=True,
        ),
    ]
