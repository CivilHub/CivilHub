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
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('checked_at', models.DateTimeField(null=True, verbose_name='read at', blank=True)),
                ('key', models.CharField(default='', max_length=32, verbose_name='keyword', blank=True)),
                ('action_verb', models.CharField(max_length=64, null=True, verbose_name='verb', blank=True)),
                ('action_object_id', models.PositiveIntegerField(null=True, blank=True)),
                ('action_target_id', models.PositiveIntegerField(null=True, blank=True)),
                ('action_actor', models.ForeignKey(related_name='made_notifications', verbose_name='actor', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('action_object_ct', models.ForeignKey(related_name='notify_action_objects', blank=True, to='contenttypes.ContentType', null=True)),
                ('action_target_ct', models.ForeignKey(related_name='notify_action_targets', blank=True, to='contenttypes.ContentType', null=True)),
                ('user', models.ForeignKey(related_name='notifications', verbose_name='user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-created_at',),
                'verbose_name': 'notification',
                'verbose_name_plural': 'notifications',
            },
            bases=(models.Model,),
        ),
    ]
