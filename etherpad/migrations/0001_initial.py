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
            name='EtherpadAuthor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('etherpad_id', models.CharField(max_length=255, blank=True)),
            ],
            options={
                'verbose_name': 'author',
                'verbose_name_plural': 'authors',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EtherpadGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('etherpad_id', models.CharField(max_length=255, blank=True)),
            ],
            options={
                'verbose_name': 'authors group',
                'verbose_name_plural': 'authors groups',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Pad',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
                ('slug', models.CharField(default='', help_text='Slug will be auto-generated if not provided', unique=True, max_length=255, blank=True)),
                ('group', models.ForeignKey(to='etherpad.EtherpadGroup')),
            ],
            options={
                'verbose_name': 'pad',
                'verbose_name_plural': 'pads',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='etherpadauthor',
            name='group',
            field=models.ManyToManyField(related_name='authors', null=True, to='etherpad.EtherpadGroup', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='etherpadauthor',
            name='user',
            field=models.OneToOneField(related_name='author', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
