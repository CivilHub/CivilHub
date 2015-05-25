# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('organizations', '0003_auto_20150508_1138'),
        ('locations', '0002_auto_20150424_1157'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Guide',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('slug', models.CharField(max_length=210, verbose_name='slug')),
                ('content', models.TextField(default='', verbose_name='content')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='last modified')),
                ('status', models.PositiveIntegerField(default=1, verbose_name='status', choices=[(1, 'draft'), (2, 'published')])),
                ('authors', models.ManyToManyField(related_name='authored_guides', null=True, verbose_name='authors', to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
                'verbose_name': 'guide',
                'verbose_name_plural': 'guides',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GuideCategory',
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
            name='GuideTag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64, verbose_name='name')),
            ],
            options={
                'verbose_name': 'tag',
                'verbose_name_plural': 'tags',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='guide',
            name='category',
            field=models.ForeignKey(related_name='guides', verbose_name='category', blank=True, to='guides.GuideCategory', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='guide',
            name='editors',
            field=models.ManyToManyField(related_name='permitted_guides', to=settings.AUTH_USER_MODEL, blank=True, help_text="Select people permitted to modify this guide. You don't have to include yourself if you're owner.", null=True, verbose_name='editors'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='guide',
            name='location',
            field=models.ForeignKey(related_name='guides', verbose_name='location', to='locations.Location'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='guide',
            name='organizations',
            field=models.ManyToManyField(related_name='guides', null=True, verbose_name='organizations', to='organizations.Organization', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='guide',
            name='owner',
            field=models.ForeignKey(related_name='owned_guides', verbose_name='owner', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='guide',
            name='tags',
            field=models.ManyToManyField(to='guides.GuideTag', null=True, verbose_name='tags', blank=True),
            preserve_default=True,
        ),
    ]
