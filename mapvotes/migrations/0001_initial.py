# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Marker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lat', models.DecimalField(verbose_name='latitude', max_digits=9, decimal_places=6)),
                ('lng', models.DecimalField(verbose_name='longitude', max_digits=9, decimal_places=6)),
            ],
            options={
                'verbose_name': 'marker',
                'verbose_name_plural': 'markers',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='date')),
                ('marker', models.ForeignKey(verbose_name='marker', to='mapvotes.Marker')),
                ('user', models.ForeignKey(verbose_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'vote',
                'verbose_name_plural': 'votes',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Voting',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=64, verbose_name='label')),
                ('description', models.TextField(default='', verbose_name='description', blank=True)),
                ('start_date', models.DateTimeField(null=True, verbose_name='start', blank=True)),
                ('finish_date', models.DateTimeField(null=True, verbose_name='finish', blank=True)),
                ('is_public', models.BooleanField(default=False, help_text='Allow other users to manage markers', verbose_name='public')),
                ('is_limited', models.BooleanField(default=False, help_text='Limit user votes to just one marker in set', verbose_name='public')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('author', models.ForeignKey(verbose_name='author', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'voting',
                'verbose_name_plural': 'votings',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together=set([('user', 'marker')]),
        ),
    ]
