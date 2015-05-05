# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SimplePoll',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('slug', models.CharField(max_length=210, verbose_name='slug')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SimplePollAnswer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(editable=False, db_index=True)),
                ('text', models.CharField(default='', max_length=255, verbose_name='answer')),
            ],
            options={
                'ordering': ('order',),
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SimplePollAnswerSet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answer', models.TextField(default='', verbose_name='answer')),
                ('poll', models.ForeignKey(verbose_name='poll', to='polls.SimplePoll')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SimplePollQuestion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('order', models.PositiveIntegerField(editable=False, db_index=True)),
                ('text', models.TextField(default='', verbose_name='question')),
                ('question_type', models.PositiveIntegerField(default=1, verbose_name='type', choices=[(1, 'single'), (2, 'multiple'), (3, 'opened')])),
                ('polls', models.ManyToManyField(to='polls.SimplePoll', null=True, verbose_name='polls', blank=True)),
            ],
            options={
                'ordering': ('order',),
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='simplepollanswerset',
            name='question',
            field=models.ForeignKey(verbose_name='question', to='polls.SimplePollQuestion'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='simplepollanswerset',
            name='user',
            field=models.ForeignKey(verbose_name='user', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='simplepollanswer',
            name='question',
            field=models.ForeignKey(verbose_name='question', blank=True, to='polls.SimplePollQuestion', null=True),
            preserve_default=True,
        ),
    ]
