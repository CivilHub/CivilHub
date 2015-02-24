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
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answer', models.CharField(max_length=256)),
            ],
            options={
                'ordering': ['answer'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AnswerSet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('answers', models.ManyToManyField(related_name='answers', to='polls.Answer', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('imagableitemmixin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='places_core.ImagableItemMixin')),
                ('title', models.CharField(max_length=128)),
                ('slug', models.SlugField(unique=True, max_length=128)),
                ('question', models.TextField()),
                ('multiple', models.BooleanField(default=False)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('location', models.ForeignKey(to='locations.Location')),
                ('tags', taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', help_text='A comma-separated list of tags.', verbose_name='Tags')),
            ],
            options={
                'ordering': ['title'],
            },
            bases=('places_core.imagableitemmixin', models.Model),
        ),
        migrations.AddField(
            model_name='answerset',
            name='poll',
            field=models.ForeignKey(to='polls.Poll'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='answerset',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='answer',
            name='poll',
            field=models.ForeignKey(to='polls.Poll'),
            preserve_default=True,
        ),
    ]
