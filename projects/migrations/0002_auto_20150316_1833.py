# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0001_initial'),
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
                ('project', models.ForeignKey(related_name='discussions', verbose_name='project', to='projects.SocialProject')),
            ],
            options={
                'verbose_name': 'discussion',
                'verbose_name_plural': 'discussions',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='socialforumentry',
            name='topic',
            field=models.ForeignKey(verbose_name='discussion', to='projects.SocialForumTopic'),
            preserve_default=True,
        ),
    ]
